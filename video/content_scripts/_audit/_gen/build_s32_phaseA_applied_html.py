#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""產生 §3.2 `ch03_chain_rule` 的 **Phase A applied 報告** HTML（一次性產生器）。

**這份報告是什麼：** 不是新的稽核稿，是「Phase A 這一輪到底改了什麼」的**總帳**——
逐步列出 A1–A5 做了什麼、判準有沒有達成、證據是哪一個 commit，並把本輪最重要的一件事
（G0 內容鎖的證據鏈：23 場 `scene_text_hash` 全程零變動，所以所有畫面／契約／唸法的改動
都沒有讓任何一次 TTS 白花）單獨成節。

**為什麼要有：** 根 `CLAUDE.md`「每完成一輪撰寫後也要產 HTML 報告」——凡完成一輪內容撰寫
都要對**實際寫入的內容**另產一份 standalone HTML（MathJax CDN、雙擊即開、框架文字繁中），
與「候選／裁決稿」分開。§3.2 的候選／裁決稿是另外兩份
（`REVIEW-…-s32-a1-alignment.html`＝A1 對齊 sign-off、`REVIEW-…-s32-narration-signoff.html`
＝合成前旁白簽核），本檔是它們之後的 applied 總帳。

**資料來源分兩類（頁面上有標）：**
  ① **即時重算**——場結構、`accent` 分布、`screen_contract` 條數、`scene_text_hash`：
     由版控檔在產生時走**閘走的同一條路**重算（`review_pack.parse_content_script` ＋
     `_screen_contract.required_steps`；`narration.parse_say` ＋ `timing.text_hash`）。
     這是 `REVIEW_GATES.md` §六 6.5「正向：用閘走的同一條路解析一次並數條數」的落地。
  ② **稽核／實跑產物**——TTS 收據、gate 輪數、回歸結果：寫在下方常數區，各自標證據
     （commit hash 或版控 REPORT 的節號）。**manifest 是 untracked output，不當相依**，
     所以本支在任何乾淨 worktree 都跑得起來。

用法：  python video/content_scripts/_audit/_gen/build_s32_phaseA_applied_html.py
輸出：  video/content_scripts/_audit/REVIEW-ch03_chain_rule-s32-phaseA-applied.html
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent                     # content_scripts/_audit/
CS = AUDIT.parent                       # content_scripts/
VIDEO = CS.parent                       # video/
sys.path.insert(0, str(VIDEO))

import yaml                                                    # noqa: E402

from pipeline import _screen_contract as sc                    # noqa: E402
from pipeline import review_pack                               # noqa: E402
from pipeline.narration import parse_say                       # noqa: E402
from pipeline.timing import text_hash                          # noqa: E402

DECK = "ch03_chain_rule"
OUT = AUDIT / f"REVIEW-{DECK}-s32-phaseA-applied.html"
STORY = VIDEO / "storyboards" / f"{DECK}.yml"
STORY_MIMO = VIDEO / "storyboards" / f"{DECK}_mimo.yml"
MD = CS / f"{DECK}.md"


# ════════════════════════════════════════════════════ 稽核／實跑產物（常數區）
# 下列每一筆都標了證據。**不要在這裡算數字**——算得出來的一律走上面的「即時重算」。

# A5-2 真合成收據（`audio_mimo/manifest.json` 的 `receipt`，2026-09-14 實跑）。
TTS = {
    "approved_max": 35,          # A5-1 報價後使用者核准的 --max-billed-calls
    "backend_calls": 30,         # receipt.backend_calls（23 場 planned ＋ 7 次 fallback）
    "backend_retries": 0,        # receipt.backend_retries
    "scene_aligned": 22,         # receipt.modes.scene_aligned
    "beats": 1,                  # receipt.modes.beats（composed_mapping_figure）
    "silent": 5,                 # receipt.modes.silent（intro 1／divider 3／outro 1）
    "fallback_scenes": ["composed_mapping_figure", "proof_delicate_bound",
                        "caution_inner_derivative"],
    "audio_seconds": 704.5,      # 23 個 content 場 audio_seconds 合計
    "audio_minutes": 11.74,
    "mock_audio_estimate": 828.0,     # A5-0 mock 對同 23 場的估時（narration.estimate_seconds）
    "mock_film_seconds": 909.9,       # A5-0 mock render 的整片長度（含家具）
}

# A5-2 之後的真音檔 1080p 全片 render（收尾當日跑完）。
FILM = {
    "seconds": 786.5, "minutes": 13.1, "mib": 30.3,
    "lufs": -19.0, "true_peak": -2.2, "mock_true_peak": -7.5,
    "sync": ["beat timing clean", "render/audio lengths clean"],
    "over_video": 0, "scenes": 28,
}

# 語速最快的四場（真音檔 wpm ＝ canonical 字數 ÷ 音訊分鐘；§3.1 基準 170 wpm 是**口語口徑**）。
FAST_SCENES = [
    ("leibniz_form", 33.7, 109, 194),
    ("example_single_composition", 29.7, 95, 192),
    ("chain_rule_statement", 24.7, 79, 192),
    ("caution_inner_derivative", 21.6, 67, 186),
]

# A1–A5 逐步表。evidence 是 commit hash（版控可追）。
STEPS = [
    {
        "id": "A1",
        "title": "內容稿對 `chapter3.tex` §3.2 做 §8 對齊",
        "did": [
            "把 `source_rev` stamp 從凍結的 legacy HTML fragment 換到 "
            "`handout/latex/src/ch03/chapter3.tex`。",
            "24 個教學單元逐一與 `chapter3.tex:208–416` 的環境對照，寫出跟改／不跟改表——"
            "**結果是 24 單元零跟改**。",
            "兩個裁決項維持不跟改：#8（skip-permission 句）、#22（“key that unlocks” 比喻）"
            "——都是影片版刻意的教學鋪陳，講義沒有不代表要刪。",
        ],
        "criteria": [
            ("`[source_rev]` WARN 消失", True, "`schema.py` 不再印 `[source_rev] 1 finding(s)`"),
            ("逐單元跟改／不跟改表寫完", True, "24 筆，全在 A1 對齊報告"),
            ("scoped 回歸 blocking 0", True, "零跟改 ⇒ 無受影響單元可審"),
            ("使用者 sign-off", True,
             "**對象是對齊報告，不是 `_narration.html`**——零跟改時後者重編後逐位元組相同"),
        ],
        "evidence": [("7eb7c34", "A1 §8 對齊"), ("e51f2ba", "merge")],
        "note": "A1 排在最前面是 §3.1 Task D 的學費：§3.1 是在四原語鋪滿 27 場**之後**才對齊講義，"
                "五個場的拍子被拉長 6–35 秒、外加 15 次 billed TTS 重合成。"
                "**在花錢、動畫面之前做完對齊，這一整類成本就不存在。**",
    },
    {
        "id": "A2",
        "title": "storyboard 更新到現行契約",
        "did": [
            "`accent:` 依語意軸全面複審——`definition` 由 **10 場收到 1 場**"
            "（只留 `remainder_form_definition`，它對位 `chapter3.tex:246` 的 `def:3.1`）；"
            "`caution_inner_derivative` 補上 `accent: caution`（對位 `:342` 的 `envcaution`）；"
            "6 個散文／Figure 場與 3 個 divider 拿掉 accent（幕級家具無可對位的講義環境）。",
            "lint **6 warning → clean**（`\\dfrac` 改 `\\tfrac`、兩處 widow line 重寫句尾）。"
            "⚠ kickoff §2.3 立檔時寫 5 條，重跑實為 6 條——漏記 `caution_inner_derivative.body`。",
            "PD1-2 用 `part:` 分頁修掉——`decomposition_strategy` 在凍結的 `procedure_steps` "
            "容量下四條出路全堵，唯一出路是拆兩場。**代價＝content 場 22 → 23＝billed call +1**，"
            "而這件事必須在 A5 之前做完，否則代價從「多一次呼叫」變成「整場重合成」。",
            "**10 份 `screen_contract` ＋ 29 條 `required_steps` ＋ `coverage_enforce` 上線**"
            "——SC 閘從此不再空轉（見下方負向對照）。",
        ],
        "criteria": [
            ("四支確定性閘 0 error", True, "schema／lint／sizecheck／`derive --check`"),
            ("pedagogy gate-1 PD／OF／SC blocking ＝ 0", True,
             "四輪 blocking **3 → 1 → 1 → 0**；advisory 5 → 5 → 1 → 2（每輪重新生成）"),
            ("`accent` 複審表逐場有結論", True, "23 content 場＋3 divider 逐場"),
        ],
        "evidence": [("f8ed626", "A2 契約升級"), ("23dd48e", "A2b `part:` 分頁＋SC 上線")],
        "note": "**判準本身被這一步推翻過一次：** A2 原訂判準寫「SC-honesty blocking ＝ 0」，"
                "但那時 deck 一份 `screen_contract` 都沒有，SC1／SC2／SC-honesty **全部空轉**，"
                "綠燈是 vacuous pass。已回寫 `REVIEW_GATES.md` §六 6.2："
                "凡以「某閘 blocking ＝ 0」為判準，**必須同時寫明該閘的武裝前提**。",
    },
    {
        "id": "A2 後補",
        "title": "`decomposition_strategy` 第 11 份契約",
        "did": [
            "補上第 11 份 `screen_contract`（**7 條 `required_steps`**），"
            "搶在工具線 r2 Task I 把 `procedure_steps` 納入 `_SCOPED_TEMPLATES` 之前補綠"
            "——否則 r2 併入 main 的當下，§3.2 會立刻紅一條。",
        ],
        "criteria": [
            ("契約總數 10 → 11、`required_steps` 29 → 36", True, "見下方即時重算表"),
            ("上游 r2 併入後 §3.2 仍綠", True, "main 紅、下游分支綠——因為下游先補了"),
        ],
        "evidence": [("30c5358", "搶在 r2 前補綠")],
        "note": "這是 §六 6.6「`main` ≠ 最新」那一條的來源：**上游只對 main 驗收自己的改動時，"
                "會看到下游早已解決的問題**，也可能漏看只有下游才踩得到的問題。",
    },
    {
        "id": "A3",
        "title": "口語單一源 `.spoken.yml` ＋ `derive_spoken`",
        "did": [
            "手寫口語單一源 `content_scripts/ch03_chain_rule.spoken.yml`"
            "（A3 首版 **363 行**；經 NFA 兩輪修正後現為 377 行）。",
            "`derive_spoken.py --check` **首跑即 `parity OK`**——每個 content `say:` 都有 spoken 對應、"
            "`{show}` marker 逐一對齊、口語端無 `$` LaTeX 外洩。",
            "23 場散文逐字相同驗證 **0 failures**（D2 的硬條件：英文散文逐字相同，"
            "只有 `$…$` 裡的 LaTeX 可以被拼成口語）。",
        ],
        "criteria": [
            ("`parity OK`", True, "首跑即過，零迭代"),
            ("`_mimo.yml` 生成", True, "`storyboards/ch03_chain_rule_mimo.yml`（DO NOT EDIT）"),
            ("口語版通讀無 LaTeX 漏出", True, "`--check` 的 `$` 掃描 ＋ 人工通讀"),
        ],
        "evidence": [("1cbff24", "A3 口語單一源＋derive")],
        "note": "`parity OK` 首跑即過的原因是 A2 已經把散文定稿了——**口語源是照著定稿的 `say:` 寫的**，"
                "不是另外寫一份再去對。順序對了，parity 就不是一道要迭代的閘。",
    },
    {
        "id": "A4",
        "title": "NFA 旁白忠實稽核（雙閘）",
        "did": [
            "**gate-1**（`narration-faithfulness-audit` subagent，Claude Opus 5，免費）："
            "**0 blocking／3 advisory**，三條全部採納；D5 新慣例"
            "（分母整體被平方的分數 → “the square of the quantity …”）入 rubric。",
            "**R2-01**（gate-1 回歸輪抓到）：gate-2 的 prompt 與 `.md` 檔頭判準**相反**"
            "——成因是**主對話派工契約寫錯**，把「核准源」欄填成內容稿，"
            "於是**付費**閘拿到相反指示。由主對話修正。",
            "**gate-2**（agy `gemini-3.1-pro-high`，計費，使用者 2026-09-14 核准）："
            "**1 blocking**（N2-01，D2 parity）、0 advisory；13 條高風險唸法逐條 PASS。"
            "修根因（把指數搬進 LaTeX）後回歸 **0/0**。",
            "**gate-2 另在 `disagreements_with_premise` 提出框架層反對**"
            "——使用者簽的是內容稿，真正被合成的是從未以「旁白」身分送簽的 `say:`。"
            "使用者裁決＝**選 B：合成前補一個 `say:` 的簽核點**。",
        ],
        "criteria": [
            ("gate-1 blocking 0", True, "3 advisory 全採納，回歸後殘留 1（R2-01）已修"),
            ("gate-2 blocking 0", True, "N2-01 修後回歸 0/0"),
            ("回歸再審確認沒改過頭／漏檔", True,
             "全 deck 掃同型破口（`$…$` 外的散文數學字被改寫）**0 處**"),
            ("版控 REPORT 寫完", True, "`REPORT-ch03_chain_rule-narration-faithfulness.md`"),
        ],
        "evidence": [("ae840f3", "gate-1 三條 advisory＋D5 入契約"),
                     ("52962e0", "R2-01 prompt 判準對齊"),
                     ("201281d", "N2-01 指數搬進 LaTeX")],
        "note": "**gate-2 的價值不只是補 gate-1 的遺漏，是不接受第一讀者與指揮者共同的灰區。** "
                "N2-01 那一處 gate-1 判 0 blocking、**主對話也看過同一處、判為灰區放過**；"
                "gate-2 判它是 blocking，而且給的修法比主對話原本採用的更好"
                "（修根因 ⇒ 口語端一字不改 ⇒ 23 場 hash 零變動）。",
    },
    {
        "id": "A5",
        "title": "TTS（唯一的大額計費點）",
        "did": [
            "**A5-0 mock 驗時序**（零計費）：`[sync] clean`、mock 整片 909.9 s。"
            "⚠ mock 的 `modes` 顯示 `scene_aligned: 0 / beats: 23` 是**假象**"
            "（靜音無從 forced-align），`--backend mimo --dry-run` 顯示 23 場全走 scene-level。",
            "**A5-1 報價**：canonical 路 722.8 s vs 口語路 730.9 s，兩路交叉驗證一致；"
            "使用者**核准上限 35**。",
            "**A5-2 真合成**：`backend_calls: 30`／`backend_retries: 0`"
            "（23 場 planned ＋ 7 次 fallback），**30 ≤ 35 核准上限**。"
            "modes＝22 scene_aligned／1 beats／5 silent（家具）；3 場走過 fallback。",
            "音訊 **704.5 s ＝ 11.74 分**，比 mock 對同 23 場的估時（828 s）**短約 15%**"
            "（逐場 −14%～−19%）——見下方「本輪學到」。",
            "**真音檔 1080p 全片 render**：成片 **786.5 s ＝ 13.1 分**、30.3 MiB；"
            "**兩道 `[sync]` 硬閘全過**（`beat timing clean` ＋ `render/audio lengths clean`），"
            "28 場**零**「narration over video」。",
        ],
        "criteria": [
            ("`manifest.json` 生成且 freshness 過", True, "`make.py --reuse-audio` 接受"),
            ("billed call ≤ 核准數", True, "**30 ≤ 35**"),
            ("`[sync]` 兩道硬閘 clean", True, "28 場零 narration-over-video"),
            ("`listening_pack` 使用者聽過並認可", False,
             "**待使用者**——這是 Phase A 最後一個停等點，見下方「待您裁決」"),
        ],
        "evidence": [],
        "note": "**真合成前必須先清掉 `audio_mimo/`，或帶 `--force-backend-switch`**"
                "——A5-0 的 mock 預設把靜音 WAV 與 mock manifest 寫進**真合成要去的同一個目錄**。"
                "本輪把 mock 產物移到 `audio_mock_pre_tts/` 留底。",
    },
]

# G0 內容鎖：hash 零變動被驗證的四個時刻。
G0_CHECKS = [
    ("A2 的 `say:` 逐字", "f8ed626 ／ 23dd48e",
     "`accent`／`part:`／`screen_contract` 全部是**畫面與契約**欄位；"
     "`part:` 分頁處只動標點與首字母大小寫（`derivative -- and` → `derivative. And`），"
     "**沒有增字、沒有刪字**。"),
    ("A2b 的 `part:` 分頁", "23dd48e",
     "`decomposition_strategy` 拆成兩場後，兩場 `say:` 合起來的 token 序列與拆前相同。"),
    ("A4 gate-1 三條 advisory 落地", "ae840f3",
     "N1-02／N1-03 只改**數學的唸法**（`$…$` 內），散文一字不動；"
     "N1-01 的裁決是兩個產物都不動、只加 doc-sync 標註。"),
    ("A4 gate-2 N2-01 修根因", "201281d",
     "把 `squared` 從散文搬進 LaTeX（`$(x+2)$ squared` → `$(x+2)^2$`）"
     "⇒ **口語文字一字不改**，兩邊散文回到逐字相同。"),
]

# 三處「由耳移到眼」（NFA 查出；與旁白簽核稿同源，此處為摘要）。
EAR_TO_EYE = [
    {
        "scene": "remainder_form_definition",
        "what": r"Definition 3.1 的式子 $f(x_0+h)=f(x_0)+m\,h+R(h)$ 與 $\lim_{h\to 0}R(h)/h=0$",
        "onscreen": True,
        "detail": "旁白只說 “…with <b>this equation</b>, where the remainder over $h$ goes to zero.”"
                  "——式子本身沒有被逐項唸出，“this equation” 是**指示詞、指向畫面**。"
                  "完整式子在該場 `statement:`，隨 `{show statement}` 上畫面。",
    },
    {
        "scene": "proof_setup_substitution ／ proof_easy_piece",
        "what": r"$m_2=f'(g(x_0))$ 的**定義**",
        "onscreen": True,
        "detail": "耳朵從頭到尾沒聽到 $m_2$ 是什麼——上一場只說 “apply its remainder form too”，"
                  "下一場直接說 “$m_2$ is a constant”。**A2b 已把 $m_2=f'(g(x_0))$ 接在 "
                  "`proof.1` 那一列的式尾**，補上這個「被命名、被當常數用，卻從未在畫面上定義」的缺口。",
    },
    {
        "scene": "proof_delicate_bound",
        "what": r"$\alpha_1$ 這個**名字**（第二次縮小窗口所取的門檻）",
        "onscreen": False,
        "detail": "gate-1 N1-02 把唸法改為 “shrinking the window once more so "
                  r"$\lvert R_1(h)/h\rvert$ is less than one”——數學等價，但 $\alpha_1$ 不再被點名，"
                  "**畫面兩列 `proof` 也沒有它**。對影片聽眾這是簡化不是缺漏"
                  "（該步驟的內容耳朵聽得到），但**若您認為證明的可追溯性需要這個名字，這一場就要改**。",
    },
]

# 本輪沒做的與為什麼。
NOT_DONE = [
    {
        "what": "`worked_example` 模板遷移（5 個 `example_*` 場維持 `derivation`）",
        "why": "**`DESIGN.md:532` 已裁決不遷**（2026-09-13）：遷移要重 derive `_mimo`，"
               "而 reveal id 改名會讓 beat 級 TTS reuse 失配。"
               "§3.2 kickoff §4 A2 第 4 點寫的卻是「例題場改 `worked_example` 模板」"
               "——**兩份同日 kickoff 對同一件事給相反指示**，子代理停下來回報才沒做錯。"
               "⇒ 已回寫 §六 6.8：凍結一份共用層／模板時要回頭改受影響的節 kickoff。",
    },
    {
        "what": "Phase B 全部（B1 原語鋪滿／B2 render＋兩道硬閘／B3 回歸輪）",
        "why": "**使用者指示停在 A5-3。** 前置條件其實已備齊"
               "（共用層 v1 已凍結於 `6c72163`、工具線 r1／r2 已併入 main），"
               "但 Phase A 的最後一道人閘（聽感）未過，G0 的門還沒關上。",
    },
    {
        "what": "`derive_spoken.py` 的 `MD_CONFIG_AND_CONVENTIONS` §二 慣例摘錄表未收 D5 新列",
        "why": "那張表是 `_narration_spoken.md` 的檔頭樣板，屬 **pipeline 共用 code**；"
               "改它會讓 §3.1 `ch03_trig_derivatives` 的生成檔一併漂移，"
               "而本輪的工作範圍不得碰 §3.1。**權威表（rubric:51）已收，摘錄表落後一列**；"
               "下次動到共用層時一併補，並同輪重生兩節的衍生檔。",
    },
]


# ═══════════════════════════════════════════════════════════════ 即時重算區
def live_facts() -> dict:
    """由版控檔重算頁面上所有「算得出來」的數字。走閘走的同一條路。"""
    sb = yaml.safe_load(STORY.read_text(encoding="utf-8"))
    scenes = sb["scenes"]
    kinds: dict[str, int] = {}
    accents: dict[str, int] = {}
    for s in scenes:
        kinds[s.get("kind", "?")] = kinds.get(s.get("kind", "?"), 0) + 1
        if s.get("accent"):
            accents[s["accent"]] = accents.get(s["accent"], 0) + 1

    parsed = review_pack.parse_content_script(MD)
    contracts = 0
    steps_total = 0
    per_unit: list[tuple[str, int]] = []
    for u in parsed["units"]:
        raw = u.get("screen_contract")
        if not raw:
            continue
        contracts += 1
        k = len(sc.required_steps(raw))
        steps_total += k
        per_unit.append((u.get("id", "?"), k))

    mimo = yaml.safe_load(STORY_MIMO.read_text(encoding="utf-8"))
    hashes: list[tuple[int, str, str, int]] = []
    for s in mimo["scenes"]:
        if s.get("kind") != "content":
            continue
        beats = parse_say(s.get("say", ""))
        joined = " ".join(b.text for b in beats)
        hashes.append((s.get("n") or len(hashes) + 1, s["id"], text_hash(joined), len(beats)))

    return {
        "scenes": len(scenes), "kinds": kinds, "accents": accents,
        "hooks": [s["id"] for s in scenes if s.get("hook")],
        "parts": sum(1 for s in scenes if s.get("part")),
        "contracts": contracts, "steps": steps_total, "per_unit": per_unit,
        "hashes": hashes,
        "meta_flags": [k for k in sb.get("meta", {}) if k.endswith("_enforce")],
    }


# ═══════════════════════════════════════════════════════════════════ 渲染
def esc(s: str) -> str:
    """只轉義 & < >，行內 $…$ 的 LaTeX 原封不動交給 MathJax。"""
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def md_inline(s: str) -> str:
    """極小的行內標記：`code` → <code>，**bold** → <b>。

    **順序：先 bold、再 code。** 反過來會壞——粗體段常常「跨過」一個 code span
    （例如 `**10 份 `screen_contract` 上線**`），先切 backtick 會把那一對 `**`
    拆到兩個不同的段裡，兩邊各自落單、兩邊都不展開。

    已經直接寫成 <b> 的地方不受影響。不碰 $…$ 的內容（那裡不會出現 `**`）。
    落單的 `**`（成對數不足）原樣還原，不吞字。
    """
    chunks = s.split("**")
    if len(chunks) % 2:                            # 成對：偶數段一般文字、奇數段粗體
        s = "".join(c if i % 2 == 0 else f"<b>{c}</b>" for i, c in enumerate(chunks))
    return "".join(p if i % 2 == 0 else f"<code>{p}</code>"
                   for i, p in enumerate(s.split("`")))


def main() -> int:
    F = live_facts()
    H: list[str] = []
    A = H.append

    A("<!DOCTYPE html>")
    A('<html lang="zh-Hant">')
    A("<head>")
    A('<meta charset="utf-8">')
    A('<meta name="viewport" content="width=device-width, initial-scale=1">')
    A("<title>§3.2 The Chain Rule — Phase A applied 總帳</title>")
    A("""<script>
  window.MathJax = {
    tex: { inlineMath: [['$','$']], displayMath: [['$$','$$']] },
    svg: { fontCache: 'global' },
    options: { skipHtmlTags: ['script','noscript','style','textarea','pre','code'] }
  };
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js" id="MathJax-script" async></script>""")
    A("<style>")
    A(CSS)
    A("</style>")
    A("</head>")
    A("<body>")
    A('<div class="wrap">')

    # ───────────────────────────────────────────── header ＋ 一句話結論
    A('<header class="top">')
    A('  <p class="eyebrow">applied 報告 · 這一輪到底改了什麼</p>')
    A("  <h1>§3.2 The Chain Rule — Phase A 總帳</h1>")
    A(f'  <p class="deck">deck <code>{DECK}</code> · 內容線 A1–A5 收案 · '
      f"2026-09-14 · <b>不是新的稽核稿</b></p>")
    A("</header>")

    A('<div class="lede">')
    A("<p><b>一句話結論：</b>Phase A 的 A1–A5 全部收案——講義對齊零跟改、storyboard 升到現行契約、"
      "口語單一源 parity 首跑即過、NFA 雙閘 blocking 歸零、23 場真音檔已合成"
      f"（<b>{TTS['backend_calls']} / {TTS['approved_max']}</b> 次呼叫、0 retry、"
      f"{TTS['audio_seconds']} s ＝ {TTS['audio_minutes']} 分）、"
      f"真音檔 1080p 成片已跑完（<b>{FILM['seconds']} s ＝ {FILM['minutes']} 分</b>，"
      f"兩道 <code>[sync]</code> 硬閘全過）；"
      "<b>全程 23 場 <code>scene_text_hash</code> 零變動</b>，所有畫面／契約／唸法的改動"
      "都沒有讓任何一次 TTS 白花。<b>唯一待辦是 A5-3 的聽感人閘</b>。</p>")
    A("<p class='muted'>本頁是 applied 總帳：逐步「做了什麼／判準有沒有達成／證據是哪一個 commit」。"
      "逐條 finding 的可讀版在各閘自己的審核稿（下方交付物清單）。</p>")
    A("</div>")

    # ───────────────────────────────────────────── 交付物清單
    A('<div class="h2">交付物清單（本輪產出）</div>')
    A('<p class="h2sub">前三份是<b>給您過目／裁決</b>的 HTML，第四份是<b>版控結案紀錄</b>，本檔是總帳。</p>')
    A('<div class="deliv">')
    for href, name, role, state in [
        (f"REVIEW-{DECK}-s32-a1-alignment.html", "A1 講義對齊報告",
         "A1 的停等點——24 單元逐一跟改／不跟改，含兩個裁決項", "✅ 使用者已 sign-off"),
        (f"REVIEW-{DECK}-s32-narration-signoff.html", "旁白簽核稿（合成前人閘）",
         "23 場 <code>say:</code> 以「旁白」身分送簽；由 gate-2 的框架層反對促成", "✅ 已簽，A5-2 才開跑"),
        (f"../../output/ch03/s3.2/audio_mimo/REVIEW-{DECK}_mimo-listening.html",
         "聽感人閘 listening pack",
         "每場 <code>&lt;audio&gt;</code>＋WPM＋validation／fallback＋LUFS，依風險排序",
         "⏳ <b>待您裁決</b>（非版控，在 output 目錄）"),
        (f"REPORT-{DECK}-narration-faithfulness.md", "NFA 版控結案報告",
         "兩道閘的 findings、裁決與 commit 索引（<code>git log --grep=\"NFA\"</code>）", "✅ 已寫完"),
    ]:
        A('  <div class="dcard">')
        A(f'    <a class="dname" href="{href}">{name}</a>')
        A(f'    <div class="drole">{role}</div>')
        A(f'    <div class="dstate">{state}</div>')
        A("  </div>")
    A("</div>")

    # ───────────────────────────────────────────── A1–A5 逐步
    A('<div class="h2">A1–A5 逐步：做了什麼／判準／證據</div>')
    A('<p class="h2sub">判準取自 <code>KICKOFF-s32-chain-rule.md</code> §4 每一步自己的「完成判準」。'
      "<b>未達成的一項用紅色標出</b>，不藏。</p>")
    for st in STEPS:
        A('<div class="step">')
        A('  <div class="shead">')
        A(f'    <span class="sbadge">{esc(st["id"])}</span>')
        A(f'    <span class="stitle">{md_inline(esc(st["title"]))}</span>')
        A("  </div>")
        A('  <div class="skey">做了什麼</div>')
        A("  <ul class='did'>")
        for d in st["did"]:
            A(f"    <li>{md_inline(d)}</li>")
        A("  </ul>")
        A('  <div class="skey">判準</div>')
        A('  <table class="crit"><tbody>')
        for text, ok, how in st["criteria"]:
            mark = '<span class="ok">達成</span>' if ok else '<span class="pend">未達成</span>'
            A(f"    <tr><td class='cm'>{mark}</td><td class='ct'>{md_inline(esc(text))}</td>"
              f"<td class='ch'>{md_inline(how)}</td></tr>")
        A("  </tbody></table>")
        if st["evidence"]:
            A('  <div class="skey">證據</div>')
            A('  <p class="ev">')
            A("    " + " · ".join(f"<code>{h}</code> <span class='evl'>{esc(lbl)}</span>"
                                  for h, lbl in st["evidence"]))
            A("  </p>")
        if st.get("note"):
            A(f'  <div class="note">{md_inline(st["note"])}</div>')
        A("</div>")

    # ───────────────────────────────────────────── G0 證據鏈
    A('<div class="h2 hot-h2">G0 內容鎖的證據鏈 — 本輪最重要的一件事</div>')
    A('<p class="h2sub"><b>命題：</b>Phase A 從頭到尾，23 個 content 場的 '
      "<code>scene_text_hash</code> <b>一次都沒有變過</b>。"
      "所以畫面欄位、契約宣告、數學唸法的每一次改動，都<b>沒有讓任何一次 TTS 白花</b>。</p>")

    A('<div class="claim">')
    A("<p><b>為什麼這件事值得單獨成節：</b>§3.1 的學費是 <b>15 次 billed call 重合成</b>"
      "——因為對齊講義排在鋪原語之後，旁白被拉長了。§3.2 把對齊排在 A1、把"
      "「只能靠改場結構關閉的 gate-1 blocking」排在 A5 之前，於是唯一一次"
      "真正的內容變動（PD1-2 的 <code>part:</code> 分頁）只讓 planned call 從 22 變成 23，"
      "<b>而不是重合成一整場</b>。</p>")
    A("<p class='muted'>驗法＝比對 <code>scene_text_hash</code>（剝掉 marker 後的口語全文 hash）。"
      "<b>不要離線直接呼叫 <code>scene_reuse_ok</code></b>——那會繞過 CLI 閘、"
      "給出與實際相反的預測（§3.1 ⑬ 花掉 13 次 billed call 的成因）。</p>")
    A("</div>")

    A('<div class="h3">被驗證的四個時刻</div>')
    A('<table class="tbl"><thead><tr><th>時刻</th><th>commit</th><th>為什麼 hash 不變</th></tr></thead><tbody>')
    for when, ev, why in G0_CHECKS:
        A(f"<tr><td><b>{md_inline(esc(when))}</b></td><td class='mono'>{esc(ev)}</td>"
          f"<td>{md_inline(why)}</td></tr>")
    A("</tbody></table>")

    A('<div class="h3">現行 23 場的 hash（產生本頁時由版控檔即時重算）</div>')
    A('<p class="h2sub">走的是 TTS 自己那條路：<code>narration.parse_say</code> → 串起 beat 文字 → '
      "<code>timing.text_hash</code>。"
      "<b>2026-09-14 收尾當日與真 <code>manifest.json</code> 逐場相同</b>"
      "（22 場 scene-level 逐位元組相同；第 23 場 <code>composed_mapping_figure</code> 走 beats 模式，"
      "manifest 無 scene 級 hash，reuse key 是 <b>beat 級</b> <code>text_hash</code>＋輸出檔路徑）。</p>")
    A('<table class="tbl hash"><thead><tr><th>#</th><th>scene id</th><th>beats</th>'
      "<th>scene_text_hash</th></tr></thead><tbody>")
    for i, (_n, sid, h, nb) in enumerate(F["hashes"], 1):
        beatsmode = " <span class='tagb'>beats 模式</span>" if sid == "composed_mapping_figure" else ""
        A(f"<tr><td class='mono'>{i:02d}</td><td class='mono sid'>{esc(sid)}{beatsmode}</td>"
          f"<td class='mono'>{nb}</td><td class='mono'>{esc(h)}</td></tr>")
    A("</tbody></table>")

    A('<div class="h3">同時被改掉的東西（都沒有動到 hash）</div>')
    A('<div class="stats">')
    for v, lbl, note in [
        (f"{F['scenes']}", "storyboard 場數",
         " ／ ".join(f"{k} {n}" for k, n in sorted(F["kinds"].items()))),
        (f"{F['contracts']}", "screen_contract 份數", f"required_steps 共 {F['steps']} 條"),
        (f"{len(F['accents'])}", "accent 語意值種類",
         " ／ ".join(f"{k} {n}" for k, n in sorted(F["accents"].items()))),
        (f"{F['parts']}", "`part:` 分頁場數", "PD1-2（2 頁）＋ 證明鏈（4 頁）"),
        (f"{len(F['hooks'])}", "客製 hook 數", " ／ ".join(F["hooks"]) or "—"),
        (f"{len(F['meta_flags'])}", "meta enforce 旗標", " ／ ".join(F["meta_flags"])),
    ]:
        A('  <div class="stat">')
        A(f'    <div class="sv">{v}</div><div class="sl">{md_inline(esc(lbl))}</div>')
        A(f'    <div class="sn">{esc(note)}</div>')
        A("  </div>")
    A("</div>")

    A('<div class="claim ok-claim">')
    A("<p><b>SC 閘確實武裝了（不是 vacuous pass）：</b>正向——用閘走的同一條路解析，"
      f"得 <b>{F['contracts']} 份契約／{F['steps']} 條 <code>required_steps</code></b>"
      "（逐 unit 條數見下）；負向對照——故意從 storyboard 拿掉一個 <code>covers</code> id，"
      "<b>閘噴 <code>ERROR [SC1]</code></b>。兩步都做過才敢說「閘看得到契約」。</p>")
    A("<p class='muted'>理由：<code>_screen_contract.parse_block()</code> 是 <b>fail-closed</b>"
      "——契約只要有一個 YAML 語法錯誤（本輪實例：<code>tex:</code> 用雙引號、值裡有 "
      "<code>\\c</code> 這種非法轉義），閘看到的是「這個 unit <b>沒有</b>契約」，"
      "訊息把人導向「去寫一份」而不是「你寫的那份解不開」。"
      "<b>「我寫了契約」與「閘看得到契約」因此脫鉤。</b></p>")
    A('<p class="perunit">')
    A("  " + " · ".join(f"<code>{esc(u)}</code> {k}" for u, k in F["per_unit"]))
    A("</p>")
    A("</div>")

    # ───────────────────────────────────────────── 由耳移到眼
    A('<div class="h2">三處「由耳移到眼」</div>')
    A('<p class="h2sub">NFA 查出：這三處的內容<b>聽不到、只看得到</b>（或兩邊都沒有）。'
      "列在這裡是因為<b>只有在 <code>say:</code> 那一份上才看得見</b>——內容稿 "
      "<code>narration:</code> 是 Stage 1 的文字，不是出片旁白。</p>")
    for e in EAR_TO_EYE:
        cls = "eye ok-eye" if e["onscreen"] else "eye no-eye"
        badge = "畫面上有" if e["onscreen"] else "畫面上也沒有"
        A(f'<div class="{cls}">')
        A(f'  <div class="ehead"><span class="ebadge">{badge}</span>'
          f'<span class="esid">{esc(e["scene"])}</span></div>')
        A(f'  <p class="ewhat">{md_inline(e["what"])}</p>')
        A(f'  <p class="edetail">{md_inline(e["detail"])}</p>')
        A("</div>")

    # ───────────────────────────────────────────── 本輪學到
    A('<div class="h2">本輪學到（會影響未來每一節的報價）</div>')
    A('<p class="h2sub">這一條不是 finding，是<b>口徑事實</b>——它會改變每一節 A5-1 報價的算法，'
      "所以寫在 applied 總帳裡而不只是 commit body。</p>")
    A('<div class="claim">')
    A("<p><b>mock 估時器系統性高估約 15%。</b>A5-0 的 mock 對同樣 23 場估 "
      f"<b>{TTS['mock_audio_estimate']:.0f} s</b>，真 Dean 音檔是 "
      f"<b>{TTS['audio_seconds']} s</b>——短 "
      f"<b>{(1 - TTS['audio_seconds'] / TTS['mock_audio_estimate']) * 100:.0f}%</b>，"
      "而且<b>逐場都短</b>（−14%～−19%），不是少數幾場拉低平均。</p>")
    A("<p>成因：<code>narration.estimate_seconds</code> 用 <b>150 wpm 吃口語版字數</b>，"
      "而 Dean 本節實測是 <b>167–194 wpm</b>。"
      "⇒ <b>拿 mock 的秒數去報 TTS 的量會系統性高估</b>；"
      "A5-1 該用的是 §3.1 實測語速換算的兩路交叉驗證"
      "（canonical 722.8 s vs 口語 730.9 s，本節實測 704.5 s，誤差 &lt;4%）。</p>")
    A("<p class='muted'>對應紀律已在 <code>REVIEW_GATES.md</code> §六 6.9 ①："
      "<b>字數與語速必須同一個口徑</b>，交叉使用（口語版字數配 canonical wpm）會高估約 24%。"
      "本條是它的姊妹條：<b>mock 的秒數不是第三個口徑，是一個會高估的估計器</b>。</p>")
    A("</div>")

    # ───────────────────────────────────────────── 沒做的
    A('<div class="h2">本輪沒做的，與為什麼</div>')
    A('<p class="h2sub">三項都是<b>刻意不做</b>，不是漏做。</p>')
    for nd in NOT_DONE:
        A('<div class="nd">')
        A(f'  <div class="ndwhat">{md_inline(nd["what"])}</div>')
        A(f'  <div class="ndwhy">{md_inline(nd["why"])}</div>')
        A("</div>")

    # ───────────────────────────────────────────── 待裁決
    A('<div class="h2 hot-h2">待您裁決 — A5-3 聽感人閘</div>')
    A('<div class="act">')
    A('  <div class="act-eyebrow">Phase A 的最後一個停等點</div>')
    A('  <div class="act-title">聽過 listening pack 之後，請給一個判斷</div>')
    A('  <div class="act-sub"><b>Go</b>（Phase A 收工、G0 的門關上、Phase B 可開）'
      "　／　<b>指名重合成哪一場</b>（逐場計費，先報量）</div>")
    A('  <div class="act-note">MiMo 非決定性——同一段文字每次合成是不同 take（±~10% 長度）。'
      "<b>滿意的 take 不要重合成。</b></div>")
    A("</div>")

    A('<div class="h3">風險提示（聽的時候特別注意這幾場）</div>')
    A('<table class="tbl"><thead><tr><th>場</th><th>為什麼要注意</th></tr></thead><tbody>')
    A("<tr><td class='mono'>composed_mapping_figure</td><td>"
      "<b>全片唯一的 beats 場</b>（4 次 fallback 後降級）。beats 模式是逐 beat 合成再串接，"
      "接縫處的語氣與呼吸與 scene-level 不同——這一場最該用耳朵確認。</td></tr>")
    A("<tr><td class='mono'>caution_inner_derivative</td><td>"
      "<b>重合成過一次</b>（fallback history 2 筆）。重合成＝不同 take，"
      "與相鄰場的語氣連貫性值得聽一次。</td></tr>")
    A("<tr><td class='mono'>proof_delicate_bound</td><td>"
      "走過 1 次 fallback（resynth）。同時它是全片符號密度最高的一場"
      r"（$\lvert R_1(h)/h\rvert &lt; 1$、$(\lvert m_1\rvert+1)\varepsilon$）。</td></tr>")
    A("</tbody></table>")

    A('<div class="h3">語速最快的四場</div>')
    A('<p class="h2sub">§3.1 的實測基準是 <b>口語口徑 170 wpm</b>（canonical 口徑 138.8 wpm）。'
      "下表的 wpm ＝ <b>canonical 字數 ÷ 音訊分鐘</b>——"
      "<b>兩個口徑不可交叉使用</b>（交叉會差 24%）。</p>")
    A('<table class="tbl"><thead><tr><th>場</th><th>音訊</th><th>字（canonical）</th>'
      "<th>wpm</th></tr></thead><tbody>")
    for sid, sec, words, wpm in FAST_SCENES:
        A(f"<tr><td class='mono'>{esc(sid)}</td><td class='mono'>{sec} s</td>"
          f"<td class='mono'>{words}</td><td class='mono hotnum'>{wpm}</td></tr>")
    A("</tbody></table>")
    A("<p class='h2sub'>四場都在 186–194 wpm，明顯高於基準——<b>不是錯，是 Dean 這幾段唸得快</b>。"
      "如果聽起來趕，指名重合成即可（該場一次 billed call）。</p>")

    A('<div class="h3">成片的響度：整合值正中目標，但 true peak 餘裕變緊</div>')
    A('<table class="tbl"><thead><tr><th>量</th><th>真音檔成片</th><th>mock 成片</th>'
      "<th>判讀</th></tr></thead><tbody>")
    A(f"<tr><td>integrated loudness</td><td class='mono'>{FILM['lufs']} LUFS</td>"
      "<td class='mono'>−19.0 LUFS</td><td><b>正中目標</b>，不需處理。</td></tr>")
    A(f"<tr><td>true peak</td><td class='mono hotnum'>{FILM['true_peak']} dBTP</td>"
      f"<td class='mono'>{FILM['mock_true_peak']} dBTP</td>"
      "<td>真人聲的瞬時峰值本來就比靜音 mock 高，<b>−2.2 dBTP 仍在安全區</b>"
      "（未破 0），但餘裕從 7.5 dB 掉到 2.2 dB。</td></tr>")
    A("</tbody></table>")
    A("<p class='h2sub'><b>給 Phase B 的注意事項：</b>這一節的 house audio 目前只有 intro／outro bed "
      "與 divider stinger；<b>Phase B 若要再疊任何音效，要先確認不會把 true peak 推破 0</b>"
      "——現在只剩 2.2 dB 餘裕，不是隨手加一層就沒事的狀態。</p>")

    # ───────────────────────────────────────────── footer
    A('<div class="foot">')
    A("<p>產生器 <code>video/content_scripts/_audit/_gen/build_s32_phaseA_applied_html.py</code>"
      "（可重跑；場結構／契約條數／hash 為即時重算，稽核與實跑數字在該檔常數區、各自標證據）。</p>")
    A("<p>驗收定義的 SSOT 是 <code>video/REVIEW_GATES.md</code> §六；"
      "本節的執行計畫是 <code>video/KICKOFF-s32-chain-rule.md</code>；"
      "抽成模板的是 <code>video/KICKOFF-section-template.md</code>。</p>")
    A("</div>")

    A("</div>")
    A("</body>")
    A("</html>")

    OUT.write_text("\n".join(H), encoding="utf-8")
    print(f"[phaseA-applied] wrote {OUT}  ({OUT.stat().st_size:,} bytes)")
    print(f"[phaseA-applied] live: {F['scenes']} scenes, {F['contracts']} contracts / "
          f"{F['steps']} required_steps, {len(F['hashes'])} content hashes")
    return 0


CSS = """
:root{
  --bg:#f6f7f9; --paper:#ffffff; --ink:#191f28; --soft:#5d6876; --faint:#8a94a3;
  --line:#e2e6ec; --line2:#eef1f5;
  --accent:#2f5fe0; --accentsoft:#eaf0ff; --accentline:#c3d4fb;
  --hot:#b4341f; --hotsoft:#fdf0ec; --hotline:#f0c3b8;
  --act:#0f766e; --actsoft:#e7f5f2; --actline:#a9dcd4;
  --codebg:#f0f2f6;
}
@media (prefers-color-scheme: dark){
  :root{
    --bg:#14171c; --paper:#1b1f26; --ink:#e6e9ee; --soft:#a3adbb; --faint:#7c8695;
    --line:#2b3139; --line2:#232830;
    --accent:#7ba2ff; --accentsoft:#1d2739; --accentline:#31456b;
    --hot:#ff9d85; --hotsoft:#2c1f1b; --hotline:#5c382e;
    --act:#5fd3c2; --actsoft:#14262a; --actline:#27524d;
    --codebg:#242a33;
  }
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0; background:var(--bg); color:var(--ink);
  font:16.5px/1.75 -apple-system,"Segoe UI",Roboto,"Noto Sans TC","Microsoft JhengHei",sans-serif;
}
.wrap{max-width:880px;margin:0 auto;padding:44px 20px 100px}
code{font-family:"Cascadia Code",Consolas,"SF Mono",monospace;font-size:.88em;
  background:var(--codebg);padding:1px 5px;border-radius:4px;word-break:break-word}
.mono{font-family:"Cascadia Code",Consolas,monospace;font-size:13px;
  font-variant-numeric:tabular-nums}
.muted{color:var(--soft);font-size:14.5px}

.top{border-bottom:2px solid var(--line);padding-bottom:18px;margin-bottom:26px}
.eyebrow{margin:0 0 8px;font-size:12.5px;font-weight:700;letter-spacing:.08em;
  text-transform:uppercase;color:var(--accent)}
h1{font-size:28px;line-height:1.3;margin:0 0 8px;letter-spacing:.01em}
.deck{margin:0;color:var(--soft);font-size:13.5px}

.lede{background:var(--paper);border:1px solid var(--line);border-left:4px solid var(--accent);
  border-radius:10px;padding:18px 22px;margin:0 0 26px}
.lede p{margin:0 0 11px}
.lede p:last-child{margin-bottom:0}

.h2{font-size:20px;margin:48px 0 6px;padding-top:15px;border-top:2px solid var(--line);font-weight:700}
.hot-h2{border-top-color:var(--hot)}
.h2sub{margin:0 0 20px;color:var(--soft);font-size:14px}
.h2sub b{color:var(--ink)}
.h3{font-size:16px;font-weight:700;margin:30px 0 8px;color:var(--ink)}

.deliv{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin:0 0 6px}
.dcard{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.dname{display:block;font-weight:700;font-size:15px;color:var(--accent);text-decoration:none;
  margin-bottom:5px;line-height:1.4}
.dname:hover{text-decoration:underline}
.drole{font-size:13px;color:var(--soft);line-height:1.6}
.dstate{font-size:12.5px;color:var(--faint);margin-top:7px;padding-top:7px;border-top:1px dashed var(--line)}

.step{background:var(--paper);border:1px solid var(--line);border-radius:11px;
  padding:17px 21px 15px;margin:14px 0}
.shead{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:12px;
  padding-bottom:10px;border-bottom:1px solid var(--line2)}
.sbadge{font-weight:700;font-size:13px;color:#fff;background:var(--accent);
  border-radius:6px;padding:2px 9px;letter-spacing:.02em;white-space:nowrap}
.stitle{font-size:17px;font-weight:700}
.skey{font-size:11.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;
  color:var(--faint);margin:14px 0 6px}
.skey:first-of-type{margin-top:0}
ul.did{margin:0;padding-left:20px}
ul.did li{margin-bottom:7px;font-size:15px;line-height:1.72}
ul.did li:last-child{margin-bottom:0}

table.crit{width:100%;border-collapse:collapse;font-size:14px}
table.crit td{padding:6px 8px;border-top:1px solid var(--line2);vertical-align:top}
table.crit tr:first-child td{border-top:none}
td.cm{width:62px;white-space:nowrap}
td.ct{width:37%}
td.ch{color:var(--soft);font-size:13.5px}
.ok{color:var(--act);font-weight:700;font-size:12.5px}
.pend{color:var(--hot);font-weight:700;font-size:12.5px}

.ev{margin:0;font-size:13.5px}
.evl{color:var(--soft);font-size:12.5px}
.note{background:var(--accentsoft);border:1px solid var(--accentline);border-radius:9px;
  padding:12px 15px;margin-top:14px;font-size:14px;line-height:1.7;color:var(--soft)}
.note b{color:var(--ink)}

.claim{background:var(--paper);border:1px solid var(--line);border-left:4px solid var(--hot);
  border-radius:10px;padding:16px 20px;margin:16px 0 22px}
.ok-claim{border-left-color:var(--act)}
.claim p{margin:0 0 10px}
.claim p:last-child{margin-bottom:0}
.perunit{font-size:12.5px;color:var(--soft);line-height:2.1}

table.tbl{width:100%;border-collapse:collapse;font-size:14.5px;margin:10px 0 6px;
  background:var(--paper);border:1px solid var(--line);border-radius:10px;overflow:hidden}
table.tbl th{background:var(--line2);text-align:left;padding:9px 13px;font-size:12.5px;
  font-weight:700;letter-spacing:.04em;color:var(--soft);text-transform:uppercase}
table.tbl td{padding:9px 13px;border-top:1px solid var(--line2);vertical-align:top;line-height:1.65}
table.hash td{padding:5px 13px;font-size:13px}
.sid{color:var(--accent)}
.hotnum{color:var(--hot);font-weight:700}
.tagb{display:inline-block;background:var(--hotsoft);border:1px solid var(--hotline);color:var(--hot);
  font-size:10.5px;font-weight:700;padding:0 6px;border-radius:5px;margin-left:6px;
  font-family:-apple-system,"Segoe UI",sans-serif;vertical-align:1px}

.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:11px;margin:12px 0 18px}
.stat{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:13px 15px}
.sv{font-size:24px;font-weight:700;letter-spacing:-.01em;font-variant-numeric:tabular-nums;line-height:1.2}
.sl{font-size:13px;color:var(--ink);margin-top:2px;font-weight:600}
.sn{font-size:11.5px;color:var(--faint);margin-top:4px;line-height:1.55}

.eye{background:var(--paper);border:1px solid var(--line);border-radius:10px;
  padding:15px 19px;margin:12px 0;border-left:4px solid var(--act)}
.no-eye{border-left-color:var(--hot)}
.ehead{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:8px}
.ebadge{font-size:11.5px;font-weight:700;letter-spacing:.05em;color:var(--act);
  background:var(--actsoft);border:1px solid var(--actline);border-radius:5px;padding:1px 8px}
.no-eye .ebadge{color:var(--hot);background:var(--hotsoft);border-color:var(--hotline)}
.esid{font-family:"Cascadia Code",Consolas,monospace;font-size:12.5px;color:var(--soft)}
.ewhat{margin:0 0 8px;font-size:16px;font-weight:600}
.edetail{margin:0;font-size:14.5px;color:var(--soft);line-height:1.75}
.edetail b{color:var(--ink)}

.nd{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:14px 18px;margin:11px 0}
.ndwhat{font-weight:700;font-size:15.5px;margin-bottom:7px}
.ndwhy{font-size:14.5px;color:var(--soft);line-height:1.75}
.ndwhy b{color:var(--ink)}

.act{background:var(--actsoft);border:1px solid var(--actline);border-radius:11px;
  padding:17px 20px;margin:18px 0;text-align:center}
.act-eyebrow{font-size:11.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--act)}
.act-title{font-size:20px;font-weight:700;margin:5px 0 5px}
.act-sub{font-size:15px;color:var(--soft)}
.act-note{font-size:12.5px;color:var(--faint);margin-top:9px}

.foot{margin-top:56px;padding-top:16px;border-top:1px solid var(--line);
  font-size:12.5px;color:var(--faint);line-height:1.8}
.foot p{margin:0 0 5px}
"""


if __name__ == "__main__":
    raise SystemExit(main())
