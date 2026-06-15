# Code2Video 研究與採納計畫

> **這份文件回答一個問題：** showlab 的 Code2Video 有哪些機制值得我們的 `video/` 產線借鏡，以及**怎麼動手做**。
>
> **定位：** 研究筆記 + 可執行的實作計畫。前半（Part A–B）是研究結論，後半（Part C–F）是逐項的實作設計，細到檔案、函式簽名、整合點、校準步驟、驗收標準，回來就能照著開工。
>
> **日期：** 2026-06-02 ·  **撰寫前讀過的程式碼：** `pipeline/blocks.py`、`pipeline/brand.py`、`pipeline/sizecheck.py`、`pipeline/lint.py`、`make.py`、`pipeline/templates/{__init__,_common,graph_focus}.py`（其餘 5 個 template、`scene.py`、`theme.py` 未逐行讀——見 Part F 動手前要確認的事）。
>
> **來源：** [github.com/showlab/Code2Video](https://github.com/showlab/Code2Video) · [arXiv 2510.01174](https://arxiv.org/abs/2510.01174) · [HF paper page](https://huggingface.co/papers/2510.01174)（NeurIPS 2025 DL4C workshop）。

---

## 回來後第一件事（quickstart）

直接從 **P0（重疊偵測 guard）** 開工——它免費、確定性、正中目前 `pipeline-hardening` 這條線，且和既有 `sizecheck.py` 是同一個建置流程。第一步先建立 baseline：

```powershell
# 現有 guard 跑得過嗎？（P0 會擴充這支）
python video\pipeline\sizecheck.py video\storyboards\ch01_inverse_functions.yml
```

然後照 **Part C → P0 → 實作步驟** 做。P0 預估半天到一天。

---

## TL;DR（結論先講）

1. **Code2Video 是「同類工具、相反哲學」。** 它是丟一個知識點 → 全自動吐出 Manim 影片的學術系統（衝 benchmark、無人介入）；我們是忠於講義、人寫內容稿、Claude 輔助、逐項簽核的單一課程精品產線。**它的「自動生成大腦」不可照搬**——會牴觸我們 [`CONTENT_METHODOLOGY.md`](CONTENT_METHODOLOGY.md) §8「內容稿是 source of truth」與 [`DESIGN.md`](DESIGN.md)「author writes storyboard by hand — NOT auto-generated」。

2. **但它的幾項工程機制正好打在我們的痛點上。** 依契合度，建議採納順序：

   | 優先 | 採納項目 | 對到我們哪裡 | 成本 | 哲學契合 |
   |---|---|---|---|---|
   | **P0** | occupancy/overlap 重疊偵測 | 擴充 `sizecheck.py` | 免費、確定性 | ★★★ |
   | **P1** | VLM Critic 視覺回饋迴路 | 補 guard 看不到的視覺缺陷 | 計費（需同意） | ★★★ |
   | **P2** | ScopeRefine 分層 auto-fix | Claude 生成 `hook` 動畫的修錯紀律 | 免費（協定為主） | ★★☆ |
   | **P3** | AES 五維評分 rubric | 人審 / Critic 的評分表 | 免費（文件） | ★★☆ |
   | **P4** | TeachQuiz（簡化版 coverage check） | 驗收「真的有教到 learning_goal」 | 計費、選用 | ★☆☆ |

3. **它反過來幫我們背書。** Code2Video 的 ablation：拿掉 Planner，美感與學習成效各崩 ~41 分。我們整套 `CONTENT_METHODOLOGY` 就是用人腦、用比 LLM 高的標準在做那個 Planner——**重押內容稿是被數據證實的對的方向**。

4. **有一軸我們其實領先，不要回退：** 旁白↔揭示的音畫對齊（每 beat 合成、量真實時長、用時長驅動 reveal hold）。Code2Video 聚焦視覺/code，這條不是它的重點。

---

# Part A — Code2Video 是什麼

## A.1 目標與哲學

把一個「知識點」自動變成 3Blue1Brown 風格的教學動畫，主張用**可執行的 code（Manim）當統一介質**，而非 pixel-space 擴散生成，換取 clarity / coherence / reproducibility。整條線無人介入。

## A.2 三 agent 架構

- **Planner** — 把知識點展開成 outline → storyboard：每節有 title、lecture lines、對應動畫；同時備齊視覺素材（asset），快取重用。
- **Coder** — 把 storyboard 變成可執行 Manim Python；內建 **scope-guided auto-fix（ScopeRefine）** 的除錯。
- **Critic** — 用 VLM（Gemini-2.5-pro）配 **visual anchor prompt** 看 render 出來的畫面，修空間排版、減少重疊與雜亂。

## A.3 關鍵機制（我們要參考的本體）

- **ScopeRefine（分層 auto-fix）：** render 失敗時不整段重生，而是 line±1 →（不行）整個 lecture-line 區塊 →（再不行）才整節重生。逐層放大、先局部後全域。論文量到比無此機制省 **1.6–1.7× token**。
- **Visual anchor + occupancy table：** 把畫布切成 **6×6 anchor 格**，每格對應固定 Manim 座標；小元素佔一格（point-level）、大元素佔一個跨格的 bounding box（region-level）。一張 **occupancy table** 記每個元素佔哪些格、縮放、對應 code 行 → 用它**偵測衝突並重新分配到空格**。ablation：6×6 是最佳折衷（8×8 太擠、太粗對不齊）。
- **Planner 的素材快取：** asset 依 prompt 分析取得，存 `D_asset` 跨節重用，避免重複生成。

## A.4 評估（值得借鏡的「概念」）

- **TeachQuiz（學習成效）：** 兩階段 unlearn→relearn。先讓模型「遺忘」某知識點測基準分 `S1`，再讓它「看影片」後只憑影片證據作答得 `S2`，分數 `S2 − S1` 就是影片帶來的學習增益。
- **AES（美感與結構）五維、各 0–100：** Element Layout（排版）、Attractiveness（吸引力）、Logic Flow（時序邏輯）、Visual Consistency（跨幀一致）、Accuracy & Depth（正確與深度）。
- **MMMC benchmark：** 117 個 3B1B 取向主題 + 人工參考影片。
- **關鍵相關性：** 人評研究發現**美感分數與 TeachQuiz 學習成效相關係數 r=0.971**——視覺清晰度直接驅動學會與否，不是裝飾。這是 P0/P1 最硬的動機。

## A.5 與我們的根本差異（決定哪些不能抄）

| 面向 | Code2Video | 我們的 `video/` |
|---|---|---|
| 起點 | 一個「知識點」字串 | `chapters/*.tex` 的一節（人讀、手寫內容稿） |
| 內容來源 | LLM 自由生成 | 忠於講義、可回溯到環境/行號 |
| 人的角色 | 無（全自動） | 主導：寫內容稿、簽核 narration 與動畫 |
| Critic | 自動改 code 的迴路 | （無——這正是 P1 要補的，但要做成**建議報告**不是自動改） |
| 旁白/音畫對齊 | 非重點 | 核心資產（每 beat 量時長驅動 reveal） |
| 目標函數 | benchmark 分數 | 單一課程的教學品質 |

> **採納原則：** 借**機制**，不借**自動化哲學**。凡是「讓 LLM 自動取代人的判斷」的部分，一律降級成「產生一份給人審的建議/檢查」，以符合我們 human-in-the-loop 的設定。

---

# Part B — 機制對照表

| Code2Video 機制 | 我們現況 | 落差 | 採納形式 |
|---|---|---|---|
| Critic：VLM 看畫面批改排版 | 只有 build-time 靜態 guard（`lint.py` 抓標記/`$`；`sizecheck.py` 抓出框、並排字級不一致、muted） | guard 抓不到**重疊、壓字、留白醜、視覺失衡** | **P0**（重疊，確定性、免費）+ **P1**（其餘，VLM、計費） |
| visual anchor + occupancy table | 已有 grid（`theme` 度量、固定 14.222×8 frame、`SAFE_MARGIN`、`SIDE_GUTTER`） | 缺「誰佔了哪塊」的帳 → 無法自動測重疊 | **P0** 的核心資料結構 |
| ScopeRefine 分層 auto-fix | Claude 生成 `hook` 動畫，失敗時無明訂修補階梯 | 容易整支重生、丟掉已簽核的部分 | **P2**（協定 + 既有 `make.py --scene` 當迴路） |
| AES 五維 rubric | 散落在 `DESIGN.md` Authoring checklist | 無單一「視覺驗收」清單 | **P3**（文件） |
| TeachQuiz | 每單元有 `learning_goal` 欄位（內容稿） | 無「影片是否真的教到」的回測 | **P4**（簡化 coverage check，選用） |
| IconFinder 素材快取 | 不需要（symbol-heavy 微積分） | — | **不採納**（Part D） |
| 全自動 Planner→Coder→Critic | 人寫內容稿 + 模板 + 簽核 | 哲學相反 | **不採納**（Part D） |

---

# Part C — 採納提案（逐項實作設計）

## P0 — Occupancy / Overlap 重疊偵測 guard ★最先做

### 動機與證據
- 我們的 guard 是 build-time/AST 檢查，抓的是「已知固定清單」：標記亂碼、`$` 不平衡、出框、並排字級不一致、教學散文用 muted。**抓不到兩個元素在畫面上重疊。**
- Code2Video 用 occupancy table 自動測重疊；我們可以做一個**確定性、零 API 成本**的版本，吻合既有「靜態 guard」路線。
- 硬動機：A.4 的 r=0.971——Element Layout 是學習成效的第一驅動力。

### 關鍵設計判斷（讀 code 後收斂）
讀 `graph_focus.py` 後發現一個會決定成敗的點：

> **圖內的「重合」是有意義的，不是 bug。** 點落在曲線上（`plot.point` on `function`）、coral guide 線穿過交點、ε-band 包住曲線——這些在 axes 座標空間裡是刻意的。對它們做重疊告警會**大量誤報**。

而且**圖與標題/註解的碰撞早已被 `_fit_graph_to_safe_zone()` 在 build 時擋掉**（它把 graph group 夾在 title 底與 annotation 頂之間並縮放）。

**結論——把重疊 guard 的範圍收斂成：只檢查「螢幕座標空間的文字/卡片排版層」，放過「axes 座標空間的圖內幾何」。** 這正是 `sizecheck` 已經在處理的同一族元素（它的 `SIBLING_PREFIXES = ("point","proof","step","annotation","row")`）。兩者互補：

- `sizecheck` 問：**並排的 sibling 字級一樣嗎？**
- overlap 問：**有任何 positioned block 在畫面上撞在一起嗎？**

真正受益的是多文字/卡片的 template：`recap_cards`、`definition_math`、`theorem_proof`、`procedure_steps`、`example_walkthrough`——free-floating 文字塊一旦定位算錯就會疊。

### 資料結構：anchor 是「報告層」，AABB 是「決策層」
- **決策用連續 AABB（axis-aligned bounding box）**：`sizecheck._overflow_issues` 已經在用 `mob.get_left()/get_right()/get_bottom()/get_top()`，精準、無量化誤差。
- **anchor 格只當「人類可讀的報告 + 未來 auto-layout 的地基」**：把 frame 量化成格子，訊息可寫「`math.1` 與 `step.2` 同佔 C3–D4」。Code2Video 的 6×6 就在同尺寸的 14.222×8 manim frame 上得出，**可直接沿用 6×6**；但因為碰撞判定走連續 AABB，**格數是低風險選擇**，不必糾結。

### 實作步驟

**Step 1｜給 `Block` 加一個 `layer` 欄位**（`pipeline/blocks.py`，1 行，向後相容）

```python
@dataclass
class Block:
    id: str
    mobject: Any
    anim: str = "write"
    static: bool = False
    layer: str = "content"   # content | background | decoration | graph
```

- `content`（預設）：title、eyebrow、statement、math.*、step.*、point.*（recap）、proof.*、annotation.*、qed——**要參與重疊檢查**。
- `background`：card、grid、全幅底——內容本來就疊在它上面，免檢。
- `decoration`：motif、reference guide（`y=x`）、純參考標籤——刻意覆蓋，免檢。
- `graph`：axes + 所有 `_plot_blocks` 產物 + ticks——axes 座標空間的幾何，內部重合有意義，整組免檢（對外碰撞已由 `_fit_graph_to_safe_zone` 擋掉）。

**Step 2｜在 template 標記 layer**（只動幾個明顯點）

- `templates/_common.py` → `motif_corner()`：`Block("motif", motif, anim="fade", static=True, layer="decoration")`
- `templates/graph_focus.py`：
  - `Block("axes", axes, …, layer="graph")`
  - `_plot_blocks()` 內每個 `Block(f"plot.{i}", …)`、`Block(f"label.{…}", …)` 加 `layer="graph"`
  - `Block("ticks", ticks, …, layer="graph")`
  - `title`、`annotation.*` 維持預設 content
- 其餘 5 個 template（未讀）：把 `math_card`/背景 `RoundedRectangle` 那種底框標 `background`。grep 線索：`brand.math_card(`、`RoundedRectangle(`、`coordinate_grid(`。
- **優雅降級：** 未標記的 template，其 block 全是 `content`；但 card 之類大底框會被 Step 3 的「containment 跳過」吃掉（大塊包小塊＝分層，不算撞）。所以 P0 能先上線，再逐步補標記。

**Step 3｜寫 `_overlap_issues()`**（`pipeline/sizecheck.py`，仿 `_overflow_issues` 結構）

```python
OVERLAP_FRAC = 0.20   # 交集 > 較小塊面積的 20% 才告警（校準後可調）

def _aabb(mob):
    try:
        x0, x1 = float(mob.get_left()[0]), float(mob.get_right()[0])
        y0, y1 = float(mob.get_bottom()[1]), float(mob.get_top()[1])
    except Exception:
        return None
    if x1 - x0 <= 1e-6 or y1 - y0 <= 1e-6:
        return None
    return (x0, x1, y0, y1)

def _area(a):       return (a[1]-a[0]) * (a[3]-a[2])
def _inter(a, b):
    ix = max(0.0, min(a[1], b[1]) - max(a[0], b[0]))
    iy = max(0.0, min(a[3], b[3]) - max(a[2], b[2]))
    return ix * iy

def _overlap_issues(scene, blocks):
    sid = scene.get("id")
    items = []
    for b in blocks:
        if getattr(b, "layer", "content") != "content":
            continue
        box = _aabb(getattr(b, "mobject", None)) if getattr(b, "mobject", None) is not None else None
        if box is not None:
            items.append((b.id, box))
    out = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            id_a, a = items[i]
            id_b, bx = items[j]
            inter = _inter(a, bx)
            if inter <= 0:
                continue
            sm, lg = min(_area(a), _area(bx)), max(_area(a), _area(bx))
            if sm <= 1e-9:
                continue
            # containment：大塊幾乎完全包住小塊 = 分層（highlight box、未標記的 card），不算撞
            if inter >= 0.95 * sm and lg > 4 * sm:
                continue
            frac = inter / sm
            if frac > OVERLAP_FRAC:
                out.append(("warn",
                    f"{sid}: blocks '{id_a}' and '{id_b}' overlap "
                    f"({frac*100:.0f}% of the smaller) -- they may collide on "
                    f"screen; reposition or split."))
    return out
```

**Step 4｜接進 `check_scenes`**（一行；緊接既有 overflow 檢查）

```python
        # -- overflow guard (every kind) ...
        issues += _overflow_issues(scene, blocks)
        # -- overlap guard: screen-space content blocks colliding --
        issues += _overlap_issues(scene, blocks)
```

`make.py` 已自動跑 `check_scenes`、errors 中止（return 2）、warns 只印——**不必改 `make.py`**。

### 校準與測試
1. 對 §1.1 全部 8 個已交付場景跑：`python video\pipeline\sizecheck.py video\storyboards\ch01_inverse_functions.yml`。
2. 這 8 個是驗證過的成片 → **理應零 overlap 告警**。任何告警＝(a) 潛藏的真 bug，或 (b) `OVERLAP_FRAC`/containment 門檻要調。逐一判讀。
3. 故意把某 storyboard 的兩個 recap point 疊在一起（暫時改 buff/座標）→ 確認 guard 抓得到（true positive）。
4. 門檻穩定、§1.1 乾淨後，考慮把嚴重重疊（如 `frac > 0.5`）升成 `error`（仿 `_overflow_issues` 的 error/warn 兩級）。**先 warn，再升 error**，比照本專案既有校準節奏。

### 風險 / 邊角
- **`transform_from_previous`：** `math` 支援這個 anim（B 元素取代 A 元素），到那拍時 A 已不在畫面 → A、B 視為同時存在會誤報。§1.1 未必用到；真的用到時，規則：同一 group 內標了 `transform_from_previous` 的 block N，不要和它的前驅 N−1 互比。先記為已知限制。
- **reveal 是累加的：** 既揭示的元素留在畫面（見 `scene.py` 語義，Part F 待確認），所以「全部 block 的聯集＝最終最滿的一幀」，對它測重疊就是測 worst case，正確。唯一例外就是上面的 transform/replace。
- **bbox 偏鬆：** `.next_to(buff=0.1)` 的相鄰塊 bbox 可能微疊 → `OVERLAP_FRAC=0.20` 容忍。

### 工作量 / 驗收
- **約 0.5–1 天。** 驗收：§1.1 八場景零誤報；人造重疊測得到；warn 訊息含兩個 block id 與重疊百分比。
- 一個 commit：`video: sizecheck overlap guard (occupancy-style, screen-space layout layer)`。

---

## P1 — VLM Critic 視覺回饋迴路 ★高價值，需 API 同意

### 動機
P0 用確定性方法吃掉**幾何重疊**那個子集；剩下需要**判斷**的缺陷——壓字到難讀、遠看字太小、留白失衡、顏色對比不足、動畫殘留雜物、跨場景風格漂移——要靠 VLM 看真畫面。這正是 Code2Video Critic 在做的事。r=0.971 是它的價值背書。

### 與 Code2Video 的關鍵差異（哲學適配）
**不做自動改 code 的迴路。** Critic 產出一份**給人審的 review 報告**（per-frame findings + 五維評分 + 建議），人（或 Claude 在人簽核下）才動手。對應 `CONTENT_METHODOLOGY` §5「生成的動畫 code SHOULD 經使用者過目認可」。VLM 提案、人定奪。

### 設計
- **不分析整支影片，只抽關鍵幀。** 每個 beat 結束時（該拍的 reveal 都落定）是構圖最滿的一刻，最容易暴露缺陷。用 `manifest.json` 的 `beats[].end_seconds` 當時間戳，`ffmpeg -ss` 從各場景 mp4（`output/_media/.../<meta_id>__<sid>.mp4`，見 `make.py` render()）抽幀。一節幾十張靜圖，遠比逐幀分析便宜。
- **給 VLM 的 context：** 幀圖 + 該場景 `title` + 該 beat 的 narration 文字（`beats[].text`）+ 該拍應已出現的元素清單。可選加 `learning_goal`（在內容稿 `.md`，非 storyboard）。
- **輸出：** 結構化 JSON（defects[] + 五維分數 + 修改建議），存 `output/<chNN>/<sX.Y>/critic/<scene>.json`，另產一份人讀的 `.md` 摘要。**純建議，不改 storyboard。**
- **評分用 A.4 的 AES 五維**，但裁成單幀可判的（EL/AT/AD 靠單幀；LF/VC 要餵連續幀序列）。

### 成本閘門（依 [`CLAUDE.md`](../CLAUDE.md) 必須做）
寫成 `pipeline/critic.py`：
- `--dry-run`：只抽幀 + 印出要送的 prompt 與幀數，**不呼叫 API**。
- 真跑前先印估算（幀數 × 模型單價）並要求 `--confirm` 才送。
- 預設一次只跑 `--scene <id>`，不要整章。
- 比照 TTS：計費路徑與免費路徑分離。

### 模型
- 最省事：沿用既有 Gemini 線（已有 `google-genai` + `GEMINI_API_KEY` 供 TTS），走 Gemini vision。
- 替代：Claude vision（本模型即可）。
- 建議拿**一個場景**做 Gemini vs Claude 的 bake-off，比排版批改品質再定。

### 與 P0 的分工（成本分層）
P0 免費、跑在每次 render 前（CI 級），吃幾何子集；P1 計費、當**週期性 review pass**，吃需要判斷的子集。先 P0 後 P1。

### 工作量 / 驗收
- 抽幀 + dry-run + 估算先做（免費，0.5 天）；bake-off 與報告格式再一輪。
- 驗收：`--dry-run` 能對 §1.1 列出每場景待審幀與 prompt；`--confirm` 後產出 JSON+MD，defects 能指到具體場景/幀。

---

## P2 — ScopeRefine 分層 auto-fix（給動畫生成的修錯紀律）

### 背景
`hook` 欄位＝「dotted path to a custom animation fn（escape hatch）」。依 `CONTENT_METHODOLOGY` §5，Claude 現在依 `animation_cue` 生成這些客製動畫 code。**生成的 code render 爆掉時，要有修補階梯，而不是整支重生。** Code2Video 量到分層修補省 1.6–1.7× token，對我們更重要的是：局部修補**保住已簽核的部分**，比整支重生再重審省事。

### 這在我們這裡主要是「協定」，不是新程式
我們的「Coder」是對話中的 Claude，不是自動 agent。所以 P2 = 一份寫進文件的修補階梯 + 善用既有工具：

**修補階梯（render 失敗時，Claude 依序嘗試）：**
1. 讀 manim traceback → 定位生成的 `hook` fn 裡的失敗行。
2. **局部修**：只改失敗行 + 緊鄰上下文，重跑。
3. 連續 N 次局部失敗 → **放大到整個 hook fn**。
4. 仍失敗 → **才從 `animation_cue` 整支重生**。
5. 每次修補要小到能被使用者**重新過目**（§5 簽核規則）。

**既有迴路就是 harness——不必另寫：**
```powershell
python video\make.py --storyboard <yml> --scene <hook場景id> --backend mock --quality low
```
`make.py` 的 render() 已 per-scene 捕捉例外、印 traceback（`traceback.print_exc()`）、`--scene` 可單跑、`mock` 不計費——這就是緊迴路。

**可選小工具：** 為每個 hook 快取「上一個能 render 的版本」，整支重生失敗時可回滾。低優先。

### 落地形式
把上面的階梯寫進 [`CONTENT_METHODOLOGY.md`](CONTENT_METHODOLOGY.md) §5（動畫生成那段）當作 Claude 的工作守則。**這是文件改動 + 紀律**，不是大工程。

---

## P3 — AES 五維 rubric 當視覺驗收清單

### 動機
Code2Video 的 AES 五維是現成、經驗證的視覺品質維度。我們的視覺檢核散在 `DESIGN.md` 的 Authoring checklist，缺一張「整支看完」的驗收表。

### 落地（純文件，低工）
把五維落成專案化的具體檢查，加進 `DESIGN.md`「Authoring checklist」之後，或 `CONTENT_METHODOLOGY` §7 之後另立「視覺 QA」：

| AES 維度 | 我們的具體檢查 |
|---|---|
| Element Layout | 無重疊（P0 已自動測）、守 `SAFE_MARGIN`、視覺平衡 |
| Attractiveness | 動畫有教學目的，不是靜態投影片（§5「Animate, not just display」） |
| Logic Flow | reveal 順序貼合 narration beats、一單元一重點 |
| Visual Consistency | accent role 一致、字型/字級一致、intro/outro 一致 |
| Accuracy & Depth | 忠於講義、數學正確、`learning_goal` 有交付 |

可同時當 P1 VLM Critic 的評分 rubric（同一張表，人審與機審共用）。

---

## P4 — TeachQuiz → 簡化版「coverage check」（選用、計費）

### 動機與裁剪
TeachQuiz 的 unlearn 階段是為了 benchmark 公平性（中和模型既有知識）——**我們不需要**，我們只想知道「這支影片有沒有把 `learning_goal` 教進去」。所以裁掉 unlearn，改成更輕、更實用的 **coverage check**：

- 讓一個模型「看影片（或讀 storyboard 的 narration + P1 抽出的關鍵幀）」，**逐個 `learning_goal` 回答：這個目標有沒有被畫面+旁白實際傳達？引用是第幾拍。**
- 輸出一張覆蓋表：每個 learning_goal → 有/無/部分 + 證據拍號。

### 定位
重型、計費，且我們是人審單一課程——**列為選用/未來**。需要時再做，設計同 P1 的成本閘門。內容稿每單元已有 `learning_goal`，是現成測源。

---

# Part D — 不採納 / 暫緩，與我們已領先之處

## 不採納
- **全自動 Planner→Coder→Critic autopilot。** 牴觸「忠於講義、人寫內容稿」的根本設定（`CONTENT_METHODOLOGY` §1、§8）。我們要的是借機制、保留人的判斷。
- **IconFinder 素材庫 + 快取。** 他們拿來塞 icon 美化通識主題；我們是 symbol-heavy 微積分，視覺以函數圖、數學式為主（§5 symbol-heavy 例外），用不到。

## 我們已領先、不要回退
- **旁白↔揭示的音畫對齊。** 每 beat 合成一段、量真實時長、用時長驅動 reveal hold（`DESIGN.md` Alignment 段，§1.1 實測對到 ~1 frame）。Code2Video 聚焦視覺/code，這條不是它的重點。**別為了向它看齊而動這套。**
- **忠於講義的可追溯性、模板化的視覺一致性、既有 lint/sizecheck guard。** 這些是它沒有、我們已有的資產。

---

# Part E — 建議實作順序、里程碑、相依

```
M0（免費，先做）  P0 重疊 guard
                  ├─ blocks.py 加 layer 欄位
                  ├─ graph_focus / _common 標 layer
                  ├─ sizecheck.py 加 _overlap_issues + 接進 check_scenes
                  └─ 對 §1.1 校準（零誤報）→ warn 上線 →（穩了）升 error
                       │
M1（免費，文件）  P3 AES 視覺 QA 清單寫進 DESIGN.md
                  P2 ScopeRefine 修補階梯寫進 CONTENT_METHODOLOGY §5
                       │
M2（需同意，計費） P1 VLM Critic
                  ├─ 抽幀 + --dry-run + 成本估算（免費先做）
                  ├─ Gemini vs Claude 一場景 bake-off
                  └─ review 報告（JSON+MD，純建議）
                       │
M3（選用，計費）  P4 coverage check（learning_goal 覆蓋回測）
```

- **相依：** P1 的抽幀邏輯可被 P4 重用；P3 的五維表可當 P1 的 rubric。先把 P1 抽幀做好，P4 幾乎免費搭順風車。
- **每個里程碑都可獨立交付、獨立 commit。** P0 一個 commit 就有立即價值，不必等後面。

---

# Part F — 動手前要確認的事（pre-flight）

撰寫本計畫時**未逐行讀**以下檔案，P0/P1 動工前花幾分鐘確認：

1. **`pipeline/scene.py`（reveal 語義）** — 確認「既揭示元素留在畫面、reveal 累加」。P0「聯集＝最終幀」的前提靠這個。若有元素會被移除/取代（fade out、transform replace），把它們從 overlap 的同時存在集合排除。
2. **其餘 5 個 template**（`definition_math`、`theorem_proof`、`procedure_steps`、`example_walkthrough`、`recap_cards`）— 找出各自的 card/背景底框 block，標 `layer="background"`。grep：`math_card(`、`RoundedRectangle(`。
3. **`pipeline/visuals/theme.py`** — 確認 `FRAME_W`、`FRAME_H`、`SAFE_MARGIN`、`SIDE_GUTTER`、`color()`、`TEX_TEXT_SCALE` 的實值（P0 訊息與 anchor 報告會用到；frame 已知為 14.222×8）。
4. **`transform_from_previous` 用量** — grep storyboard 看 §1.1 是否用到；用到才需要實作前驅排除規則。
5. **P1 抽幀** — 確認 `output/_media/` 下各場景 mp4 命名（`<meta_id>__<sid>.mp4`）與 `manifest.json` 的 `beats[].end_seconds` 對得起來（`make.py` render()/synth_scene() 已寫，複查即可）。

---

# 附錄

## 我這次讀過、可信賴的依據
- 程式碼：`pipeline/blocks.py`（`Block` dataclass、`play_block`）、`pipeline/brand.py`（視覺原語、`_mark_prose` 標記先例）、`pipeline/sizecheck.py`（`check_scenes`、`_overflow_issues`、`_prose_nodes`）、`pipeline/lint.py`（severity 兩級、訊息風格）、`make.py`（orchestrator、guard 呼叫點、render/synth）、`pipeline/templates/{__init__,_common,graph_focus}.py`（`build_blocks` 派發、`Block(id, …)` 產生點、graph 內幾何）。
- 專案文件：[`DESIGN.md`](DESIGN.md)、[`CONTENT_METHODOLOGY.md`](CONTENT_METHODOLOGY.md)、[`README.md`](README.md)。

## 外部來源
- [github.com/showlab/Code2Video](https://github.com/showlab/Code2Video)
- [arXiv 2510.01174 — Code2Video: A Code-centric Paradigm for Educational Video Generation](https://arxiv.org/abs/2510.01174)
- [HF paper page](https://huggingface.co/papers/2510.01174)
- 機制細節（ScopeRefine 三層、6×6 anchor、TeachQuiz、AES 五維、ablation 數字、r=0.971）取自上述論文之 method 與 experiment 章節。
