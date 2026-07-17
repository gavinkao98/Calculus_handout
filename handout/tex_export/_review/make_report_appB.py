#!/usr/bin/env python3
"""產 LaTeX pilot v2 的 appB 對照報告（standalone HTML，雙擊即開）。

    python make_report_appB.py

比照 CLAUDE.md「給使用者審核的交付物要用『打開就能讀』的形式」：繁中框架、
數學走 MathJax CDN、圖片相對路徑引用 img/（appB-html-*.png／appB-tex-*.png，
由 print_html.mjs＋pdftoppm 產出）。
"""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
IMG = HERE / "img"


def pages(prefix):
    return sorted(IMG.glob(f"{prefix}-*.png"), key=lambda p: p.name)


html_pages, tex_pages = pages("appB-html"), pages("appB-tex")

# 完整性閘數字**實跑取得**，不硬編碼（gate-2 M-B3 A3：上一版硬寫的抽取假象數
# 在 needspace 修復重編後已 stale——分頁變了，pill 被切開的位置也變）。
_cp = subprocess.run(
    [sys.executable, str(HERE.parent / "check_prose.py"), "appB",
     str(HERE.parent / "build" / "appB" / "appendixB.pdf")],
    capture_output=True, text=True, encoding="utf-8")
_cp_out = (_cp.stdout or "") + (_cp.stderr or "")
assert _cp.returncode == 0, f"check_prose FAIL——報告拒絕產出：\n{_cp_out}"
N_WORDS = re.search(r"fragment 散文詞 (\d+)", _cp_out).group(1)
_m_art = re.search(r"(\d+) 處 pdftotext 抽取假象", _cp_out)
N_ART = _m_art.group(1) if _m_art else "0"

GATES = [
    ("前置閘", "sampler 樣張使用者拍板（D10）", "v4／判斷點 1–7", "PASS"),
    ("編譯閘", "lualatex 0 error", "0", "PASS"),
    ("編譯閘", "log 無 missing character", "0", "PASS"),
    ("版面閘", "Overfull \\hbox &gt; 2pt", "0（總 overfull 亦 0）", "PASS"),
    ("版面閘", "Underfull 需目視項", "0", "PASS"),
    ("完整性閘", "轉換器節點交代率", "440 mapped / 0 skipped", "PASS"),
    ("完整性閘", "數學恰好依序還原一次（封閉不變式）", "317 / 317", "PASS"),
    ("完整性閘", f"散文依序比對（{N_WORDS} 詞）", "0 處真落差", "PASS"),
    ("測試", "golden tests＋不變式（含 appB 全篇）", "79 / 79", "PASS"),
    ("人眼閘", "appB 全 14 頁逐頁過目", "無異常", "PASS"),
]

FINDINGS = [
    ("F1", "pdftotext 抽取假象（備查，非內容問題）",
     "pill kicker（<code>STRATEGY</code>／<code>PAUSE</code>…）帶字距，"
     "<code>pdftotext</code> 會抽成分散字母（如 <code>s t r at e gy</code>）。完整性閘的"
     f"二次確認（純字母串包含）逐條驗過：<b>{N_ART} 處全數內容在</b>，0 處真落差"
     "（此數字由報告產生器實跑 <code>check_prose.py</code> 取得，隨重編自動更新）。",
     "備查即可，無需動作。"),
    ("F2", "needspace 病理（M-B3 抓到並修復的真 bug，工程紀錄）",
     "初次組裝時每個節標題都被推去新頁。以 <code>\\tracingpages</code> 定位：needspace 套件的"
     "「彈性膠水＋負 penalty」誘餌斷點是全頁唯一便宜的斷點（c=2161 vs 其他 c=100000），"
     "頁面只要在不可伸展的散文處溢出，斷點就被吸過去。sampler 沒踩到純屬運氣"
     "（它的溢出點落在 tcolorbox 的 breakable 膠水上）。修法＝棄用 needspace，"
     "改 <code>\\cb@needspace</code> 硬檢查（剩餘不足才 \\newpage、足夠則不留任何 node）；"
     "修後全 14 頁節標題貼流正常，四閘重跑全綠。",
     "備查即可；rollout 各章沿用此實作。"),
    ("F3", "兩側視覺節奏不同（拍板結果，非缺陷）",
     "LaTeX 側行距 16pt（2026-07-17 經典教科書對標拍板⑨）、上下邊距 17/23mm（⑩）；"
     "HTML 側維持 18.6pt／20/20mm。逐頁對照時右側明顯更密、版心更高，"
     "這是拍板的預期差異——密度紅利即來自於此（20 頁 → 14 頁）。",
     "對照時請以「內容一致性」為準，不必期待兩側同頁碼。"),
]

rows = "\n".join(
    f'<tr><td class="g">{g}</td><td>{k}</td><td class="num">{v}</td>'
    f'<td class="ok">{s}</td></tr>' for g, k, v, s in GATES)

findrows = "\n".join(
    f'<div class="finding"><h3><span class="fid">{fid}</span> {title}</h3>'
    f'<p>{body}</p><p class="ask"><b>處置：</b>{ask}</p></div>'
    for fid, title, body, ask in FINDINGS)

maxp = max(len(html_pages), len(tex_pages))
pairs = []
for i in range(maxp):
    h = (f'<img loading="lazy" src="img/{html_pages[i].name}">'
         if i < len(html_pages) else '<div class="none">（HTML 側無此頁）</div>')
    t = (f'<img loading="lazy" src="img/{tex_pages[i].name}">'
         if i < len(tex_pages) else '<div class="none">（LaTeX 側無此頁——內容已在前面排完）</div>')
    pairs.append(f'<div class="pg"><div class="pgno">第 {i + 1} 頁</div>'
                 f'<div class="two"><figure>{h}<figcaption>HTML（瀏覽器排版，18.6pt）</figcaption></figure>'
                 f'<figure>{t}<figcaption>LaTeX（lualatex，16pt 拍板）</figcaption></figure></div></div>')

doc = f"""<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<title>LaTeX pilot v2 對照報告 — Appendix B</title>
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
 th{{background:#f7f8fa}} .num{{font-variant-numeric:tabular-nums}}
 .g{{color:#82868f}} .ok{{color:#04773b;font-weight:600}}
 .hero{{display:flex;gap:22px;margin:18px 0}}
 .card{{flex:1;border:1px solid #e5e7eb;border-radius:10px;padding:16px 18px;background:#fbfcfd}}
 .card b{{display:block;font-size:32px;color:#0068a7;font-variant-numeric:tabular-nums}}
 .card span{{color:#565a63;font-size:13px}}
 .finding{{border:1px solid #e5e7eb;border-left:4px solid #6453a7;border-radius:8px;
      padding:12px 18px;margin:12px 0;background:#faf9fd}}
 .finding h3{{font-size:15px;margin:4px 0 6px}}
 .fid{{background:#6453a7;color:#fff;border-radius:99px;padding:2px 9px;font-size:12px;margin-right:6px}}
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

<h1>HTML→LaTeX 出版排版 pilot v2 — Appendix B 對照報告</h1>
<p class="sub">KICKOFF-latex-pilot.md 的 M-B3 交付物 · 分支 <code>handout/latex-pilot</code> ·
內容源＝<code>fragments/appB/</code>（未改動一個字元）· 模板＝<code>template/calcbook.sty</code>
（M-B1 拍板 v4，memoir＋NCM＋vendored Inter）</p>

<div class="note"><b>這份報告要你做的事：</b>看下面的逐頁對照，做 pilot 的
<b>GO（全面 rollout 到其他章）／NO-GO（回兩階段案）</b>裁決。三條 finding（F1–F3）皆為備查，
無需個別裁決。</div>

<h2>1. 一句話結論</h2>
<p>同樣的內容（一字未動、數學逐位元組相同），<b>LaTeX 以 14 頁排完 HTML 要 20 頁的內容（−30%）</b>，
所有驗收閘全綠。密度來自兩處：TeX 的全段斷行＋斷字＋microtype（ch03 pilot 已證的 ~11%），
加上 M-B1 拍板的行距 16pt／邊距 17-23mm（經典教科書對標，你在樣張上逐項拍的）。</p>

<div class="hero">
  <div class="card"><b>20 → 14</b><span>頁數（HTML → LaTeX），同內容同版心寬</span></div>
  <div class="card"><b>317 / 317</b><span>數學恰好依序還原一次（pass-through 鐵律）</span></div>
  <div class="card"><b>0</b><span>error／missing char／overfull／散文落差</span></div>
</div>

<div class="note"><b>Codex gate-2 覆核紀錄（M-B2＋M-B3，兩輪）：</b>
第一輪對 M-B1 模板判 5 blocking＋8 advisory（簽名歧義／objectives 槽缺席／figure API 缺席／頁眉
慣例註解不符／跨頁行為無樣張證據），全數修畢並回歸覆核關閉。第二輪對 M-B2＋M-B3 判
<b>1 blocking＋3 advisory</b>：blocking＝style 白名單可被結構節點與重複屬性繞過（唯讀探針實證
<code>article style</code>／<code>li style</code>／雙 style 併寫皆放行）——已修：白名單收口到
parser 層對所有節點一體把關、重複屬性一律硬錯，並補 6 條負測鎖住；advisory＝objectives schema
未封閉（已修：開場多個素 ul 硬錯）、測試覆蓋缺口（已修：mapped 鎖實值 440、<code>\\hk*</code>
禁用斷言）、報告數字硬編碼且 F1 已 stale（已修：本報告的完整性閘數字改為產生器實跑
<code>check_prose.py</code> 注入）。修正後回歸：79/79 tests 綠、appB 重轉換與修正前輸出逐位元組
相同（style 收口不影響合法內容）、四閘證據不變。</div>

<h2>2. 驗收閘（kickoff §4.5）</h2>
<table><tr><th>閘</th><th>判準</th><th>實測</th><th>結果</th></tr>
{rows}
</table>

<h2>3. Findings（皆備查，無需裁決）</h2>
{findrows}

<h2>4. 逐頁對照（HTML 左／LaTeX 右）</h2>
<p class="sub">兩側頁數差 6 頁是<b>拍板的預期結果</b>（F3）——同一序號的兩頁自第 2 頁起漸次錯開，
不是內容遺漏（完整性閘：散文 0 落差、數學 317/317 逐位元組相同）。抽樣公式對照建議看：
第 5/7 頁（\\(\\sqrt2\\) 證明、aligned 歸納）、第 8 頁（置中量詞句）、第 13 頁（underbrace）。</p>
{"".join(pairs)}

</body></html>
"""

out = HERE / "REVIEW-latex-pilot-appB.html"
out.write_text(doc, encoding="utf-8")
print("wrote", out)
print(f"  HTML {len(html_pages)} 頁 / LaTeX {len(tex_pages)} 頁")
