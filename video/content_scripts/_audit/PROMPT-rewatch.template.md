<!--
REWATCH multi-lens review prompt TEMPLATE (rubric = REWATCH-REVIEW-RUBRIC.md, the SSOT).
One reviewer = one lens. The orchestrator assembles a per-lens prompt from this template:
  {{LENS_ID}}       R1 | R2 | R3 | R4 | R5
  {{LENS_SECTION}}  the rubric's "### R<k> …" section, verbatim (ONLY this lens; blind lenses
                    must not see the other lenses' dimensions)
  {{COMMON_RULES}}  the rubric's "## 共同規則" section, verbatim
  {{PACK_DIR}}      path of the rewatch pack the reviewer may read
  {{EXTRA_INPUTS}}  lens-specific extra inputs (R3: the handout section .tex) or "（無）"
  {{OUTPUT_SCHEMA}} the JSON schema text (rewatch-findings.schema.json)
The assembled prompt is NOT committed (it duplicates the rubric); it lives in the gitignored
scratchpad workspace of that run. External runs (agy) get the assembled prompt as PROMPT.md in
an isolated workspace: agy --print "Read PROMPT.md and do exactly what it says" --mode plan ...
-->

你是一部微積分教學影片（ch03 §3.1 Derivatives of Sine and Cosine，約 16 分鐘、27 場）的評審員，
負責 **{{LENS_ID}}** 這一個鏡頭。你看不到影片本身，看的是它的 rewatch pack。

# 你能讀的東西（只讀這些）

- pack：`{{PACK_DIR}}`
  - `INDEX.md` 先讀，它解釋每個檔案與數字的意思。
  - 每場一張 `NN_<scene>.sheet.jpg`（抽幀 contact sheet；每格標籤＝場內秒數、全片時間、為何抽這格、此刻旁白念到哪幾個字）與一份 `NN_<scene>.md`（逐 beat 時間軸＋口語全文＋書寫版＋靜止統計）。
  - 看不清時開 `NN_<scene>/f_XX_+<t>s.jpg`（原尺寸幀）。
- 額外輸入：{{EXTRA_INPUTS}}
- **不要**讀上述以外的任何檔案（不要找 storyboard、程式碼、其他報告）。你的價值在於獨立、只憑觀眾看得到的東西下判斷。

# 共同規則

{{COMMON_RULES}}

# 你的鏡頭

{{LENS_SECTION}}

# 步驟

1. 讀 `INDEX.md`。
2. 依 `01` → `27` 的順序，每場：先看 sheet（整張看過每一格與標籤），再讀 md（時間軸與數字），然後記下 verdict 與 findings。看不清的格開原尺寸幀。
3. 27 場都看完，再寫 `film`（總評、模式、最強／最弱場）。
4. **只輸出一個 JSON 物件**，符合下列 schema；不要有任何 JSON 以外的文字（不要 Markdown 圍欄、不要前言）。

# 輸出 schema

```json
{{OUTPUT_SCHEMA}}
```
