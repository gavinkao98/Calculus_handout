# NTU 數學組 — Calculus Video System · Direction B（Blueprint Grid）
## 給 manim 實作的交接包

每支影片的流程：**intro（淺）→ teaching frames（暗）→ outro（淺）**。
淺＝品牌時刻（開場／收尾）。暗＝教學主體。
一節即一支影片，因此 `section_transition` 已**棄用**（僅保留於原始碼供參考）。

畫布：**1920 × 1080**，16:9。

---

## 1. `tokens.json` — 設計變數（純文字）
所有顏色（角色名稱 + 十六進位）、字型家族 + 字重、1920×1080 下的 px 字級
比例、版面邊界／gutter、圓角／描邊，以及 motif／glow 規格。
這是各項數值的精確真實來源——請從這裡量測，而非從 PNG 量測。

`video-system.css`（在 `source/` 中）是同一組 token 以即時 CSS 自訂屬性
（`:root`）呈現，若你偏好以 CSS 閱讀它們的話。

## 2. `screenshots/` — 每個場景一張 PNG（視覺參考）
| 檔案 | 模板 | export |
|---|---|---|
| 01-intro | intro（淺，彩色 lockup） | `B_IntroLight` |
| 02-definition_math | definition | `B_Definition` |
| 03-example_walkthrough | example | `B_Example` |
| 04-procedure_steps | procedure | `B_Procedure` |
| 05-theorem_proof | theorem + proof | `B_Theorem` |
| 06-recap_cards | recap | `B_Recap` |
| 07-graph_focus | 滿框 plot | `B_Graph` |
| 08-outro | outro（淺，彩色 lockup） | `B_OutroLight` |

（PNG 為寬約 924px 的視覺參考。要取得精確的像素位置，請使用原始碼 +
token，它們承載真實的 1920×1080 數值。）

## 3. `source/` — 未打包的原始原始碼（純 .jsx / .css / .html / .svg）
這不是一個獨立／自解壓的 bundle。直接在瀏覽器中開啟
`Direction B Library.html` 即可看到每個模板的實況。

| 檔案 | 內容 |
|---|---|
| `video-system.css` | 所有設計 token（`:root`）、框類別、字體與顏色工具類別、KaTeX 尺寸、glow 效果 |
| `lib.jsx` | 共用基本元件：`tex`/`M`（KaTeX）、`Eyebrow`、`HeadingRule`、`PlotDot`、`CornerTicks`、`SummitBars`、`Logo`、`LogoPlaque`、`BrandMark` |
| `graph.jsx` | `ParabolaPlot`（軸／曲線／空心點／虛線輔助） |
| `dir-b.jsx` | `B_IntroLight`、`B_Definition`、`B_OutroLight`、`B_Graph`、`B_SceneHead` |
| `dir-b-templates.jsx` | `B_Example`、`B_Procedure`、`B_Theorem`、`B_Recap`、`B_Transition`（已棄用） |
| `overview.jsx` | 「Global Visual System」規格板 |
| `design-canvas.jsx` | 審查畫布外殼（manim 不需要） |
| `assets/brand/` | 官方校徽 SVG：`lockup-color`、`lockup-white`、`lockup-mono`、`icon-color`、`icon-white`、`icon-mono` |

### Logo 使用規則
- **淺色框（intro/outro）：** `lockup-color.svg` / `icon-color.svg`——官方
  彩色標誌直接置於紙張底（#eef1f6）上，不加白底框。
- **暗色教學框：** `icon-white.svg` 反白標誌，置於右下角，低不透明度。
- 彩色標誌的墨色為海軍藍／紅／金，**僅**供淺色底使用——絕不在沒有淺色
  襯底的情況下置於暗色畫布上。

---

## 給 manim 的註記
- 數學**全程為 LaTeX**（此處透過 KaTeX / Computer Modern render）。請使用
  同樣的 TeX 字串——它們就內嵌在 JSX 中。
- 那條被強調的單一「key line」使用金色 glow（token 中的 `glow_accent`）
  作為 Manim flash/indicate 的靜態替身。
- `SummitBars` 是品牌 **motif**（上升的長條 + 選用的金星），**不是**
  logo——可安全地動畫化／重繪。`assets/brand/*` 的 SVG 才是真正的 logo，
  不得重新上色或變形。
- 明暗切換每支影片只各發生一次（開場／收尾）——在這兩個切點做 0.3–0.5 秒
  的 cross-fade，可使亮度變化不致突兀。
