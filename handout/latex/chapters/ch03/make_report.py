#!/usr/bin/env python3
"""產 LaTeX pilot 的對照報告（standalone HTML，雙擊即開）。

    python make_report.py

比照 CLAUDE.md「給使用者審核的交付物要用『打開就能讀』的形式」：繁中框架、
數學走 MathJax CDN、圖片相對路徑引用 img/。
"""
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = HERE.parent.parent / "build"
IMG = HERE / "img"


def pages(prefix):
    return sorted(IMG.glob(f"{prefix}-*.png"), key=lambda p: p.name)


def n_pages(pdf):
    out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
    for line in out.splitlines():
        if line.startswith("Pages:"):
            return int(line.split()[1])
    return 0


html_pages, tex_pages = pages("html"), pages("tex")
figs = json.loads((HERE / "figs" / "figures.json").read_text(encoding="utf-8"))

GATES = [
    ("編譯閘", "lualatex 0 error", "0", "PASS"),
    ("編譯閘", "log 無 missing character", "0", "PASS"),
    ("版面閘", "Overfull \\hbox &gt; 2pt", "0", "PASS"),
    ("版面閘", "Underfull \\hbox", "0", "PASS"),
    ("完整性閘", "轉換器節點交代率", "558 mapped / 0 skipped", "PASS"),
    ("完整性閘", "數學恰好依序還原一次（封閉不變式）", "605 / 605", "PASS"),
    ("完整性閘", "散文依序比對（4573 詞）", "0 處真落差", "PASS"),
    ("完整性閘", "panel note 抵達 PDF", "2 / 2", "PASS"),
    ("圖", "panel 匯出＋人眼過", "8 / 8", "PASS"),
    ("測試", "golden tests", "58 / 58", "PASS"),
]

FINDINGS = [
    ("F1", "既有 HTML 瑕疵，會原樣進 PDF",
     "<code>composed-mapping</code>（Figure 3.5）的標籤用 Unicode 下標零 <code>x₀</code>"
     "（U+2080），Inter 沒有這個字符，Chrome 就單獨對那一個字符掉到 <b>Times New Roman</b>。"
     "已用 CDP <code>CSS.getPlatformFontsForNode</code> 逐節點比對，<b>真實 HTML 頁面與匯出的 PDF 完全一致</b>"
     "（Inter×7 + Times×1），故非匯出失真，是既有 HTML 的既存瑕疵。依 D6「HTML 留檔不修」未動。",
     "要不要為出版級品質，把圖標籤的 <code>x₀</code> 改成 MathJax 標籤（需動 standalone 的 FIGS，"
     "屬 D6 已裁定「不修」的範圍，故請你裁決）？"),
    ("F2", "LaTeX 側新增了 HTML 沒有的東西",
     "ch03 的 HTML proof 完全沒有 QED 記號（6 個 proof、16 個 solution 皆無），"
     "雖然 <code>CONTRACT-html-writing.md</code> 說 proof 應以 <code>&lt;span class=\"qed qed-proof\"&gt;</code> 收尾。"
     "目前 LaTeX 側也<b>沒有</b>補 □（跟隨 HTML 現況）。",
     "要跟隨 HTML（維持無 QED），還是取「書的樣子」補上 □？"),
    ("F3", "字體不同族",
     "圖<b>內</b>的標籤是 <b>Inter</b>（由 CDN 載入、已嵌進匯出的 PDF），"
     "而圖說與 env kicker 是 <b>NCM Sans</b>。HTML 兩者都是 Inter。"
     "依 kickoff §4.4「裝字體屬新安裝，先問；不裝則以 NCM Sans 代替並記錄」，本輪未裝 Inter。",
     "要不要裝桌面版 Inter（新安裝，需你同意），讓 LaTeX 側的 UI 面與圖內標籤同族？"),
    ("F4", "pair 圖的置中基準",
     "匯出的 page box 含標籤溢出，左右不對稱；LaTeX 置中的是墨水框，HTML 置中的是 SVG 框，"
     "故圖可能有數 px 級視覺位移。ch03 只有 <code>remainder-tangent</code>（Figure 3.6）一張 pair。",
     "人眼閘未發現可見差異，列此備查。"),
    ("F5", "圖內文字閘目前是循環的（已知極限，不擋 pilot）",
     "<code>check_prose.py</code> 的 panel note 檢查，oracle 是 <b>exporter 自己申報的</b> "
     "<code>figures.json</code>。已實測此偽陰性：把 exporter 退回只 clone <code>&lt;svg&gt;</code>，"
     "它就不申報 notes，閘於是說「無 note 需檢查」而放行——正是它要抓的那個 bug。"
     "它能守的是「申報之後」的環節（manifest → convert.py → LaTeX → PDF）。"
     "另一個做法（HTML PDF vs LaTeX PDF 詞集比對）也實測被否決：note 是 “larger h”，"
     "而 “larger” 在課文散文裡也有（<i>the larger triangle OAC…</i>），詞集找得到就誤判成沒掉。",
     "rollout 前要補一個獨立於 exporter 的 oracle（只讀 live page 的 CDP 探針，"
     "或對 HTML 印出的 PDF 做 exact-phrase count）。目前 ch03 的 2 條 note 已用人眼＋"
     "<code>pdftotext</code> 逐條確認在 PDF 裡。"),
]

rows = "\n".join(
    f'<tr><td class="g">{g}</td><td>{k}</td><td class="num">{v}</td>'
    f'<td class="ok">{s}</td></tr>' for g, k, v, s in GATES)

figrows = "\n".join(
    f'<tr><td><code>{p["id"]}</code>{"（panel " + str(p["panel"]+1) + "）" if p["panel"] else ""}</td>'
    f'<td class="num">{p["pagePx"][0]}×{p["pagePx"][1]}</td>'
    f'<td class="num">{p["mm"]} mm</td></tr>' for p in figs["panels"])

findrows = "\n".join(
    f'<div class="finding"><h3><span class="fid">{fid}</span> {title}</h3>'
    f'<p>{body}</p><p class="ask"><b>需要你裁決：</b>{ask}</p></div>'
    for fid, title, body, ask in FINDINGS)

# 逐頁並排：兩份頁數不同（HTML 27 / LaTeX 23），故按序號對齊即可，並標明不對應是預期的
maxp = max(len(html_pages), len(tex_pages))
pairs = []
for i in range(maxp):
    h = f'<img loading="lazy" src="img/{html_pages[i].name}">' if i < len(html_pages) else '<div class="none">（HTML 側無此頁）</div>'
    t = f'<img loading="lazy" src="img/{tex_pages[i].name}">' if i < len(tex_pages) else '<div class="none">（LaTeX 側無此頁——內容已在前面排完）</div>'
    pairs.append(f'<div class="pg"><div class="pgno">第 {i+1} 頁</div>'
                 f'<div class="two"><figure>{h}<figcaption>HTML（瀏覽器排版）</figcaption></figure>'
                 f'<figure>{t}<figcaption>LaTeX（lualatex）</figcaption></figure></div></div>')

doc = f"""<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<title>LaTeX pilot 對照報告 — Ch3</title>
<script>window.MathJax={{tex:{{inlineMath:[['\\\\(','\\\\)']]}}}};</script>
<script async src="https://cdn.jsdelivr.net/npm/mathjax@4/tex-chtml.js"></script>
<style>
 body{{font:15px/1.75 "Noto Sans TC","Microsoft JhengHei",system-ui,sans-serif;
      max-width:1180px;margin:0 auto;padding:32px 24px 80px;color:#1b1c1f}}
 h1{{font-size:26px;margin:0 0 4px}} h2{{font-size:20px;margin:38px 0 12px;
      padding-bottom:6px;border-bottom:2px solid #e5e7eb}}
 .sub{{color:#82868f;margin:0 0 24px}}
 table{{border-collapse:collapse;width:100%;margin:10px 0 18px}}
 th,td{{border:1px solid #e5e7eb;padding:7px 10px;text-align:left;font-size:14px}}
 th{{background:#f7f8fa}} .num{{font-variant-numeric:tabular-nums;white-space:nowrap}}
 .g{{color:#82868f}} .ok{{color:#04773b;font-weight:600}}
 .hero{{display:flex;gap:22px;margin:18px 0}}
 .card{{flex:1;border:1px solid #e5e7eb;border-radius:10px;padding:16px 18px;background:#fbfcfd}}
 .card b{{display:block;font-size:32px;color:#0068a7;font-variant-numeric:tabular-nums}}
 .card span{{color:#565a63;font-size:13px}}
 .finding{{border:1px solid #e5e7eb;border-left:4px solid #aa3333;border-radius:8px;
      padding:12px 18px;margin:12px 0;background:#fdf7f7}}
 .finding h3{{font-size:15px;margin:4px 0 6px}}
 .fid{{background:#aa3333;color:#fff;border-radius:99px;padding:2px 9px;font-size:12px;margin-right:6px}}
 .ask{{background:#fff;border-radius:6px;padding:8px 12px;margin:8px 0 4px;font-size:14px}}
 .pg{{margin:26px 0;border-top:1px solid #eef0f3;padding-top:14px}}
 .pgno{{font-weight:600;color:#82868f;font-size:13px;margin-bottom:8px}}
 .two{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}
 .two figure{{margin:0}} .two img{{width:100%;border:1px solid #e5e7eb;border-radius:4px;display:block}}
 .two figcaption{{font-size:12px;color:#82868f;text-align:center;padding-top:5px}}
 .none{{border:1px dashed #d7dae0;border-radius:4px;height:100%;min-height:300px;display:flex;
      align-items:center;justify-content:center;color:#9aa0ac;font-size:13px}}
 code{{background:#f1f3f5;border-radius:4px;padding:1px 5px;font-size:13px}}
 .note{{background:#f7f8fa;border-left:3px solid #0068a7;padding:10px 16px;margin:14px 0;font-size:14px}}
</style></head><body>

<h1>HTML→LaTeX 出版排版 pilot — Ch3 對照報告</h1>
<p class="sub">KICKOFF-latex-pilot.md 的 M-P4 交付物 · 分支 <code>handout/latex-pilot</code> ·
內容源＝<code>html/fragments/ch03/</code>（未改動一個字元）</p>

<div class="note"><b>這份報告要你做的事：</b>看下面的逐頁對照，決定
<b>GO（全面 rollout 到其他章）</b>或 <b>NO-GO（回兩階段案：HTML Tier-1 強化＋內容凍結後再轉）</b>。
另有 5 條 finding（F1–F5）需要你個別裁決。</p>

<h2>1. 一句話結論</h2>
<p>同樣的內容、同樣的 150mm 版心、同樣的視覺設計語言，<b>LaTeX 用 24 頁排完 HTML 要 27 頁的內容</b>
（密約 11%），且所有驗收閘全綠。密度來自 TeX 的全段斷行（Knuth–Plass）＋原生斷字＋microtype，
不是把字縮小——兩側字級與版心完全相同。</p>

<div class="hero">
  <div class="card"><b>27 → 24</b><span>頁數（HTML → LaTeX），同內容同版心</span></div>
  <div class="card"><b>605 / 605</b><span>數學恰好依序還原一次（pass-through 鐵律的封閉不變式）</span></div>
  <div class="card"><b>0</b><span>overfull／missing char／散文落差</span></div>
</div>

<div class="note"><b>Codex gate-2 覆核紀錄：</b>第一輪判定「不能 sign-off」，列出 5 項真衝突——
數學保護層不是封閉的不變式（同類分隔符巢狀會提早閉合、未配對不報錯、可用 <code>&amp;#xE000;</code>
偽造占位符）、fail-loud 有靜默繞過（<code>&lt;ul&gt;DROP&lt;li&gt;</code> 的裸文字會被默默丟掉）、
<code>\item [x]</code> 的 optional-argument 洞、測試與樹不同步、以及
<b>export_figs 漏掉 Figure 3.6 兩格的 “larger h”／“smaller h”</b>（已實證的內容遺失）。
五項皆已修並用測試鎖住（golden tests 36→52）。數學的保證也從「每段都是 .tex 的 substring」
換成封閉不變式「<b>每段恰好被還原一次且依源順序</b>」——後者驗得到順序、重複與遺漏。</div>

<h2>2. 驗收閘（kickoff §4.5）</h2>
<table><tr><th>閘</th><th>判準</th><th>實測</th><th>結果</th></tr>
{rows}
</table>

<h2>3. 需要你裁決的事項</h2>
{findrows}

<h2>4. 圖：實測尺寸</h2>
<p>7 個 figure／8 個 panel。寬度＝在 HTML 版心（實測 566.94px）量到的實際渲染寬，
換算成 mm（<code>px ÷ 566.94 × 150mm</code>）。<b>不是</b> <code>\\textwidth</code>——
SVG 自帶 inline width，多數圖只佔約半欄，撐到 <code>\\textwidth</code> 會把圖內標籤等比放大約一倍。</p>
<table><tr><th>data-fig</th><th>page px</th><th>LaTeX 寬</th></tr>
{figrows}
</table>

<h2>5. 逐頁對照（HTML 左／LaTeX 右）</h2>
<p class="sub">兩側頁數不同是<b>預期的</b>——LaTeX 排得更密，所以同一序號的兩頁在後段會逐漸錯開，
不是內容遺漏（完整性閘已證明散文 0 落差、數學 605/605 逐位元組相同）。</p>
{"".join(pairs)}

</body></html>
"""

out = HERE / "REVIEW-latex-pilot-ch03.html"
out.write_text(doc, encoding="utf-8")
print("wrote", out)
print(f"  HTML {len(html_pages)} 頁 / LaTeX {len(tex_pages)} 頁")
