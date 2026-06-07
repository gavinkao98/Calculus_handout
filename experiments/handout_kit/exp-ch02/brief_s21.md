# Direction Brief — §2.1 The Tangent Line and the Derivative at a Point

> Approved at ③ direction gate. Reconstructed from conversation record.

---

## 手稿盤點
- 切線定義（極限形式 `lim_{x→a} (f(x)−f(a))/(x−a)`）
- h-form 替代寫法 `lim_{h→0} (f(a+h)−f(a))/h`
- `f'(a)` 記號引入（作為斜率別名，非函數）
- Worked example: `y = 3/x` at `(3, 1)`（有理函數，通分化簡）
- Exercise: `y = √x` at `(1, 1)`（根式）
- 一行備注：zoom-in 後曲線看起來像直線

## 薄度剖析
| 區塊 | 狀態 |
|---|---|
| 動機／為何要切線 | **薄**（手稿直接跳定義，沒鋪墊 0/0 碰撞） |
| 割線→切線直覺 + 圖 | **薄→無**（有文字但沒有 convergence 圖） |
| Worked examples | **薄**（1 worked + 1 exercise，教科書密度不足） |
| f'(a) 的詮釋 | **薄**（一行帶過） |
| 應用／具體錨 | **無** |

## 範圍與深度
- 只到「一點的導數 f'(a)」（一個數字）；不進「導函數 f'(x)」（→ §2.2 forward-ref）
- 不證極限存在性；不給 ε-δ 嚴格定義
- 結構結果（Definition 2.1）直接陳述、不另證

## 承重直覺
0/0 碰撞：天真地「用一個點算斜率」→ `(f(a)−f(a))/(a−a) = 0/0` → 需要割線的 workaround → 再取極限。先用碰撞打臉、再形式化。

## worked example 清單
| # | 函數 | 點 | 技巧 | 來源 |
|---|---|---|---|---|
| Ex 2.1 | `y = x²−3x` | `(2, −2)` | 多項式展開 | **expansion:example（新增）** |
| Ex 2.2 | `y = 3/x` | `(3, 1)` | 有理函數通分 | 手稿 |
| Ex 2.3 | `y = √(x+1)` | `(3, 2)` | 根式共軛 | **expansion:example（新增）** |
| Ex 2.4 | `y = x²` | `(1, 1)` | 數值割線→切線（表格 `h→0`）| **expansion:example（新增，批准 2026-06-07；不同題型）** |
| Ex 2.5 | `y = 1/x` | `(2, ½)` | 切線近似估 `1/2.05` | **expansion:example（新增，批准 2026-06-07；不同題型）** |

序列：多項式 → 有理 → 根式（代數求切線）→ 數值收斂（Ex 2.4）→ 切線近似（Ex 2.5，接 Remark 2.2 bookend）

> **修定（2026-06-07）：** 原 Exer 2.1–2.3（your-turn 換數字題）已移除——不符「自創題須與既有 example 不同題型、且寫成含解 worked example」政策（見 RULE.md §2、brief_s22 題目政策）。改以 Ex 2.4（數值收斂）、Ex 2.5（切線近似）兩個不同題型的 worked example 取代。連帶：§2.2 例題序 +2（見 brief_s22）。

## history / application
- **開場錨**（application）：「估算 √4.01」——真實、具體、串 local linearity
- **收尾 bookend**：Remark 2.2 回到 √4.01，用切線近似得 2.0025（四位小數正確）
- 歷史：無自然觸發，留白

## 強調 / takeaway
- **概念樞紐**：切線斜率 = 差商的極限（極限的角色：把「不可能」的 0/0 變「可計算」的值）
- **可攜技能**：用定義算切線斜率的三步法——展開 f(a+h)→ 化簡消 h → 取極限

## 刻意不寫
| 不寫什麼 | 理由 | 它該去哪 |
|---|---|---|
| 導函數 f'(x) 作為函數 | 本節 f'(a) 只是一個數 | §2.2 |
| 微分法則（power/product/quotient） | 未引入 | §2.4–§2.5 |
| ε-δ 極限嚴格定義 | 超出本節深度 | Ch1 或附錄 |
| 一般 differentiability 判準 | 需要導函數概念 | §2.3 |
| Leibniz/Newton 歷史 | 無自然觸發，留白 | — |

## 篇幅帶
3–5 A4 頁（實際產出 5 頁 print）
