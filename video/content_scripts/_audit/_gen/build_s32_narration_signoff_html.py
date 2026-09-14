#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""產生 §3.2 `ch03_chain_rule` 的**旁白簽核稿** HTML（一次性產生器）。

為什麼有這支：NFA gate-2（agy `gemini-3.1-pro-high`）在 `disagreements_with_premise`
提出——使用者簽核的是**內容稿**，但真正會被 MiMo 合成、會被觀眾聽見的是 storyboard 的
`say:`（Stage 2 為口說重寫，從未以「旁白」身分送簽）。使用者裁決＝**選 B：合成前補一個
`say:` 的簽核點**。這支就是那道人閘的產物。決策紀錄見
`_audit/REPORT-ch03_chain_rule-narration-faithfulness.md` §5。

**資料源＝canonical storyboard 的 23 個 content 場 `say:`**（不是內容稿 `.md`）。
口語版取自 `content_scripts/ch03_chain_rule.spoken.yml`。

刻意**不**改共用的 `pipeline/narration_review.py`：那支只讀內容稿 `.md`，讀不到
storyboard `say:`，且屬工具線；本輪只需要一支一次性產生器。

用法：  python video/content_scripts/_audit/_gen/build_s32_narration_signoff_html.py
輸出：  video/content_scripts/_audit/REVIEW-ch03_chain_rule-s32-narration-signoff.html
"""
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent                     # content_scripts/_audit/
CS = AUDIT.parent                       # content_scripts/
VIDEO = CS.parent                       # video/
STORY = VIDEO / "storyboards"

DECK = "ch03_chain_rule"
OUT = AUDIT / f"REVIEW-{DECK}-s32-narration-signoff.html"

# 秒數口徑：§3.1 實測語速 2,229 字 / 963.6 s => 138.8 wpm（video/KICKOFF-s32-chain-rule.md:148）。
# 本頁的逐場秒數一律以 **canonical 字數** 換算，不與口語版字數混用。
WPM_CANON = 138.8
# mock render 的口徑（pipeline/narration.py:62 `estimate_seconds` 預設）＝ 150 wpm，
# 吃的是**口語版**字數。兩個口徑都列在總覽，避免讀者把兩者混起來。
WPM_MOCK = 150.0

MARKER = re.compile(r"\{[^}]*\}")

# --- mock render 實測（主對話 2026-09-14 跑的離線 mock，本 worktree 無 build 產物可覆核）---
MOCK_RENDER_SECONDS = 909.9


def esc(s: str) -> str:
    """只轉義 & < >，讓行內 $…$ 的 LaTeX 原封不動交給 MathJax。"""
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def strip_markers(say: str) -> str:
    """剝掉 {show …} reveal marker，收斂空白成單一段流暢文字。"""
    return " ".join(MARKER.sub(" ", say).split())


def wc(text: str) -> int:
    return len(strip_markers(text).split())


def load_yaml(p: Path):
    return yaml.safe_load(p.read_text(encoding="utf-8"))


# ---------------------------------------------------------------- 手寫內容區塊
# 以下三段是 NFA 稽核的裁決產物，不是從 YAML 推得的，故寫在這裡。

# 「你不會聽到的東西」——NFA 查出的三處「由耳移到眼」。
EAR_TO_EYE = [
    {
        "scene": "remainder_form_definition",
        "what": "Definition 3.1 的式子 $f(x_0+h)=f(x_0)+m\\,h+R(h)$ 與 "
                "$\\lim_{h\\to 0} R(h)/h = 0$",
        "spoken": "旁白只說 “…if there’s a number $m$ and a function $R$ with "
                  "<b>this equation</b>, where the remainder over $h$ goes to zero.” "
                  "——式子本身<b>沒有被逐項唸出</b>，“this equation” 是指示詞，指向畫面。",
        "onscreen": "<b>有。</b>完整式子在該場的 <code>statement:</code>，隨 "
                    "<code>{show statement}</code> 上畫面；$m=f'(x_0)$ 與 tangent-line "
                    "拆解圖在 <code>math.0</code>／<code>math.1</code>。",
        "judge": "聽者只聽得到「有這麼一條式子，且餘項除以 $h$ 趨近零」的<b>語意</b>，"
                 "聽不到符號本身。耳眼合起來才是完整的定義。",
    },
    {
        "scene": "proof_setup_substitution ／ proof_easy_piece",
        "what": "$m_2=f'(g(x_0))$ 的<b>定義</b>",
        "spoken": "`proof_setup_substitution` 的旁白只說 “apply its remainder form too”，"
                  "沒有為 $m_2$ 命名；下一場 `proof_easy_piece` 直接說 "
                  "“<b>$m_2$ is a constant</b>”。也就是說，$m_2$ 是什麼，<b>耳朵從頭到尾沒聽到</b>。",
        "onscreen": "<b>有（A2b 補的）。</b>2026-09-14 把 "
                    "$m_2=f'(g(x_0))$ 接在 <code>proof.1</code> 那一列的式尾，"
                    "補上這個「被命名、被當常數用，卻從未在畫面上定義」的缺口。",
        "judge": "這是本節最需要「耳眼合看」的一處：只聽不看，"
                 "$m_2$ 會是一個憑空出現的常數。",
    },
    {
        "scene": "proof_delicate_bound",
        "what": "$\\alpha_1$ 這個<b>名字</b>（第二次縮小窗口所取的門檻）",
        "spoken": "旁白改說 “…and <b>shrinking the window once more</b> so the absolute "
                  "value of the ratio of $R_1(h)$ to $h$ is less than one…”——"
                  "數學等價，但 $\\alpha_1$ <b>不再被點名</b>。",
        "onscreen": "<b>沒有。</b>畫面兩列 <code>proof</code> 也未出現 $\\alpha_1$；"
                    "講義（`chapter3.tex`）有這個名字，影片版兩端都以「再縮一次窗口」的說法代替。",
        "judge": "對影片聽眾這是<b>簡化，不是缺漏</b>——該步驟的內容（取更小的門檻使 "
                 "$\\lvert R_1(h)/h\\rvert &lt; 1$）耳朵聽得到；只是那個希臘字母沒有被引入。"
                 "若您認為證明的可追溯性需要這個名字，這一場就要改。",
    },
]

# 「本輪對旁白動過什麼」——與 07 月那版的差異。
CHANGES = [
    {
        "tag": "分場",
        "scene": "decomposition_strategy",
        "body": "用 <code>part:</code> 拆成兩場（<code>decomposition_strategy</code> 1/2 ＋ "
                "<code>decomposition_strategy_repeat</code> 2/2）。接縫處："
                "<code>derivative -- and</code> → <code>derivative. And</code>"
                "——只動<b>標點與首字母大小寫</b>，<b>沒有增字、沒有刪字</b>。",
    },
    {
        "tag": "唸法",
        "scene": "proof_delicate_bound",
        "body": "口語端把 $\\lvert R_1(h)\\rvert/\\lvert h\\rvert$ 改唸成 "
                "$\\lvert R_1(h)/h\\rvert$ 的形（NFA gate-1 N1-02，D4：主詞與動詞原本相距 23 字）。"
                "<b>數學等價、散文一字未動</b>。",
    },
    {
        "tag": "唸法",
        "scene": "example_chain_times_quotient",
        "body": "口語端把 $3/(x+2)^2$ 改唸成 “the square of the quantity x plus two”"
                "（NFA gate-1 N1-03，D3：原唸法的 “squared” 右界沒關，會被聽成 "
                "$\\bigl(3/(x+2)\\bigr)^2$）。<b>散文未動</b>。",
    },
    {
        "tag": "書寫",
        "scene": "example_chain_times_quotient",
        "body": "NFA gate-2 N2-01：把 <code>say:</code> 的 <code>$(x+2)$ squared</code> "
                "改成 <code>$(x+2)^2$</code>，讓 <code>squared</code> 不再是 "
                "<code>$…$</code> 外的散文字。<b>口語文字一字未改</b>，"
                "<b>朗讀出來完全一樣</b>——只是修掉一個 register 破口。",
    },
    {
        "tag": "零改動",
        "scene": "其餘 22 場",
        "body": "除上述以外，<b>旁白英文一個字都沒改</b>。2026-09-14 的 A1 上游對齊"
                "（`chapter3.tex` 只動標點平實化／同義詞／圖說精簡）結論＝"
                "<b>24 個單元零跟改</b>（A1 §8）。",
    },
]


def build() -> int:
    canon = load_yaml(STORY / f"{DECK}.yml")
    spoken = load_yaml(CS / f"{DECK}.spoken.yml")

    scenes = canon["scenes"]
    content = [s for s in scenes if s.get("kind") == "content"]
    dividers = [s for s in scenes if s.get("kind") == "divider"]
    if len(content) != 23 or len(dividers) != 3:
        print(f"[signoff] 場數不符：content={len(content)} divider={len(dividers)}"
              f"（預期 23／3）", file=sys.stderr)
        return 1

    total_canon = sum(wc(s.get("say", "")) for s in content)
    total_spoken = sum(wc(spoken.get(s["id"], "")) for s in content)
    est_canon_s = total_canon / WPM_CANON * 60.0
    est_mock_min = total_spoken / WPM_MOCK

    H: list[str] = []
    A = H.append

    # ------------------------------------------------------------------ head
    A('<!DOCTYPE html>')
    A('<html lang="zh-Hant">')
    A('<head>')
    A('<meta charset="utf-8">')
    A('<meta name="viewport" content="width=device-width, initial-scale=1">')
    A('<title>§3.2 The Chain Rule — 旁白簽核稿（合成前人閘）</title>')
    A('''<script>
  window.MathJax = {
    tex: { inlineMath: [['$','$']], displayMath: [['$$','$$']] },
    svg: { fontCache: 'global' },
    options: { skipHtmlTags: ['script','noscript','style','textarea','pre','code'] }
  };
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js" id="MathJax-script" async></script>''')
    A('<style>')
    A(CSS)
    A('</style>')
    A('</head>')
    A('<body>')
    A('<div class="wrap">')

    # ------------------------------------------------------------ 1. 開場說明
    A('<header class="top">')
    A('  <p class="eyebrow">合成前人閘 · NFA gate-2 框架層裁決（選 B）的落地</p>')
    A('  <h1>§3.2 The Chain Rule — 旁白簽核稿</h1>')
    A(f'  <p class="deck">deck <code>{DECK}</code> · 資料源 '
      f'<code>video/storyboards/{DECK}.yml</code> 的 23 個 content 場 <code>say:</code></p>')
    A('</header>')

    A('<section class="lede">')
    A('  <p><b>這一頁是什麼。</b>這是 §3.2 影片<b>真正會被唸出來的那 23 段旁白</b>的全文，'
      '按出片順序排好，數學已渲染成看得懂的樣子。</p>')
    A('  <p><b>為什麼現在要簽。</b>您在 2026-06-29 簽核的是<b>內容稿</b>；'
      '而 Stage 2 為了「說出來順」把它重寫過，實際送去合成的是 storyboard 的 <code>say:</code>'
      '——這份文字<b>從未以「旁白」的身分送到您面前</b>。NFA gate-2 指出了這個落差，'
      '您的裁決是：<b>合成之前補簽一次</b>。這一頁就是那一次。</p>')
    A('  <p><b>簽完會發生什麼。</b>這 23 段文字會被送去 MiMo 合成語音，'
      '<b>花 23 次計費呼叫</b>。此後任何一個字的改動，都要把那一場<b>重新合成、重新計費</b>。'
      '<span class="hot">現在改是零成本。</span></p>')
    A('</section>')

    # ------------------------------------------------------------ 2. 總覽數字
    A('<section class="stats">')
    for label, value, note in [
        ("content 場數", "23", "另有 intro 1／divider 3／outro 1，皆無旁白"),
        ("canonical 字數", f"{total_canon:,}", "storyboard <code>say:</code>，剝掉 <code>{show}</code> marker"),
        ("口語版字數", f"{total_spoken:,}", "同一批話攤成口語後的字數（送 TTS 的那串）"),
        ("旁白秒數（估）", f"{est_canon_s:.0f} s", f"canonical 字數 ÷ {WPM_CANON} wpm（§3.1 實測語速）"),
        ("成片長度（估）", f"{est_mock_min:.1f} 分", f"口語版字數 ÷ {WPM_MOCK} wpm（mock 口徑）"),
        ("mock render 實測", f"{MOCK_RENDER_SECONDS:.1f} s", "離線靜音 mock 的成片長度，含 intro／divider／outro 家具"),
    ]:
        A(f'  <div class="stat"><div class="sv">{value}</div>'
          f'<div class="sl">{label}</div><div class="sn">{note}</div></div>')
    A('</section>')
    A('<p class="caliper"><b>秒數口徑（請注意不要混用）。</b>'
      f'下面<b>每一場</b>標的秒數，一律是 <b>canonical 字數 ÷ {WPM_CANON} wpm × 60</b>'
      '——§3.1 實測語速換算，逐場可加總。'
      f'總覽裡的「成片長度（估）」走的是另一個口徑（口語版字數 ÷ {WPM_MOCK} wpm，'
      '<code>pipeline/narration.py</code> 的 <code>estimate_seconds</code> 預設），'
      '因為那是 mock render 用的模型；兩個數字不同是口徑不同，不是矛盾。</p>')

    # -------------------------------------------------------- 3. 逐場旁白正文
    A('<h2 class="h2">逐場旁白（出片順序）</h2>')
    A('<p class="h2sub">這是本頁的主體。請當成老師會<b>唸出來</b>的話來讀——'
      '順不順、清不清楚、有沒有哪一句您想改。灰底的可摺疊區塊是'
      '<b>MiMo 實際要唸的那一串</b>（數學已攤成英文字），想確認某個式子會被唸成什麼時再展開。</p>')

    n = 0
    for s in scenes:
        kind = s.get("kind")
        if kind == "divider":
            A(f'''<div class="act">
  <div class="act-eyebrow">{esc(s.get("eyebrow", ""))} · 幕界</div>
  <div class="act-title">{esc(s.get("title", ""))}</div>
  <div class="act-sub">{esc(s.get("subtitle", ""))}</div>
  <div class="act-note">此為分幕卡，<b>無旁白</b>（{s.get("duration", 0)} 秒靜場）</div>
</div>''')
            continue
        if kind != "content":
            continue
        n += 1
        sid = s["id"]
        say = strip_markers(s.get("say", ""))
        spk = strip_markers(spoken.get(sid, ""))
        words = len(say.split())
        secs = words / WPM_CANON * 60.0
        A('<section class="scene">')
        A(f'  <div class="shead"><span class="snum">{n:02d}</span>'
          f'<span class="sid">{esc(sid)}</span>'
          f'<span class="tmpl">{esc(s.get("template", ""))}</span>'
          f'<span class="metrics">{words} 字 · 約 {secs:.0f} 秒</span></div>')
        A(f'  <div class="stitle">{esc(s.get("title", ""))}</div>')
        A(f'  <p class="say">{esc(say)}</p>')
        A('  <details class="spoken">')
        A('    <summary>口語版（MiMo 實際要唸的那一串）</summary>')
        A(f'    <p class="spk">{esc(spk)}</p>')
        A('  </details>')
        A('</section>')

    # --------------------------------------------- 4. 「你不會聽到的東西」
    A('<h2 class="h2">你不會聽到的東西</h2>')
    A('<p class="h2sub">下面三處，<b>某個東西從「耳朵」移到了「眼睛」</b>——'
      '旁白沒有唸，只在畫面上。這種落差最容易拖到聽感關卡才被發現，所以先攤在這裡：'
      '請看「畫面上有沒有」那一欄，判斷<b>耳朵＋眼睛合起來</b>夠不夠。</p>')
    for item in EAR_TO_EYE:
        A('<section class="gap">')
        A(f'  <div class="gap-head"><code>{esc(item["scene"])}</code></div>')
        A(f'  <p class="gap-what"><span class="tagx">移走的是</span> {item["what"]}</p>')
        A(f'  <p class="gap-row"><span class="k">耳朵聽到的</span>{item["spoken"]}</p>')
        A(f'  <p class="gap-row"><span class="k">畫面上有沒有</span>{item["onscreen"]}</p>')
        A(f'  <p class="gap-row"><span class="k">怎麼判</span>{item["judge"]}</p>')
        A('</section>')

    # ------------------------------------------- 5. 本輪對旁白動過什麼
    A('<h2 class="h2">本輪對旁白動過什麼</h2>')
    A('<p class="h2sub">與 2026 年 7 月那一版相比，旁白只有下面這些變化。</p>')
    A('<div class="chg-list">')
    for c in CHANGES:
        A('  <div class="chg">')
        A(f'    <div class="chg-head"><span class="chg-tag">{esc(c["tag"])}</span>'
          f'<code>{esc(c["scene"])}</code></div>')
        A(f'    <p>{c["body"]}</p>')
        A('  </div>')
    A('</div>')

    # ------------------------------------------------- 6. 給使用者的問題
    A('''<section class="ask">
  <h2>請您裁決</h2>
  <ol>
    <li><b>這 23 場旁白，可以拿去合成嗎？</b></li>
    <li><b>有沒有哪一場要改？</b>（請指出場 id 與想改的句子）</li>
  </ol>
  <p class="ask-note">現在改<b>零成本</b>；合成之後再改，該場要<b>重新合成、重新計費</b>。</p>
</section>''')

    A(f'''<footer class="foot">
  本檔由 <code>_audit/_gen/build_s32_narration_signoff_html.py</code> 從
  <code>storyboards/{DECK}.yml</code>（canonical <code>say:</code>）＋
  <code>content_scripts/{DECK}.spoken.yml</code>（口語版）編譯產生，改稿後重跑即同步。
  緣由與裁決紀錄見 <code>_audit/REPORT-{DECK}-narration-faithfulness.md</code> §5。
  場次：content 23／divider 3。
</footer>''')

    A('</div>')
    A('</body>')
    A('</html>')

    OUT.write_text("\n".join(H) + "\n", encoding="utf-8")
    print(f"[signoff] wrote {OUT}")
    print(f"[signoff] content 場 {len(content)}／divider {len(dividers)}；"
          f"canonical {total_canon} 字／口語版 {total_spoken} 字；"
          f"旁白估 {est_canon_s:.1f} s；成片估 {est_mock_min:.2f} 分")
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
.wrap{max-width:840px;margin:0 auto;padding:44px 20px 100px}
code{font-family:"Cascadia Code",Consolas,"SF Mono",monospace;font-size:.88em;
  background:var(--codebg);padding:1px 5px;border-radius:4px;word-break:break-word}

.top{border-bottom:2px solid var(--line);padding-bottom:18px;margin-bottom:26px}
.eyebrow{margin:0 0 8px;font-size:12.5px;font-weight:700;letter-spacing:.08em;
  text-transform:uppercase;color:var(--accent)}
h1{font-size:28px;line-height:1.3;margin:0 0 8px;letter-spacing:.01em}
.deck{margin:0;color:var(--soft);font-size:13.5px}

.lede{background:var(--paper);border:1px solid var(--line);border-left:4px solid var(--accent);
  border-radius:10px;padding:18px 22px;margin:0 0 26px}
.lede p{margin:0 0 11px}
.lede p:last-child{margin-bottom:0}
.hot{color:var(--hot);font-weight:700}

.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(158px,1fr));gap:11px;margin:0 0 14px}
.stat{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:13px 15px}
.sv{font-size:23px;font-weight:700;letter-spacing:-.01em;font-variant-numeric:tabular-nums;line-height:1.2}
.sl{font-size:13px;color:var(--ink);margin-top:2px;font-weight:600}
.sn{font-size:11.5px;color:var(--faint);margin-top:4px;line-height:1.5}
.caliper{background:var(--accentsoft);border:1px solid var(--accentline);border-radius:9px;
  padding:12px 16px;font-size:13.5px;color:var(--soft);margin:0 0 34px}
.caliper b{color:var(--ink)}

.h2{font-size:20px;margin:44px 0 6px;padding-top:14px;border-top:2px solid var(--line)}
.h2sub{margin:0 0 22px;color:var(--soft);font-size:14px}
.h2sub b{color:var(--ink)}

.act{background:var(--actsoft);border:1px solid var(--actline);border-radius:11px;
  padding:16px 20px;margin:30px 0 18px;text-align:center}
.act-eyebrow{font-size:11.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--act)}
.act-title{font-size:20px;font-weight:700;margin:5px 0 3px}
.act-sub{font-size:14px;color:var(--soft)}
.act-note{font-size:12px;color:var(--faint);margin-top:7px}

.scene{background:var(--paper);border:1px solid var(--line);border-radius:11px;
  padding:17px 21px 13px;margin:14px 0}
.shead{display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin-bottom:4px}
.snum{font-variant-numeric:tabular-nums;font-weight:700;font-size:12.5px;color:var(--soft);
  border:1px solid var(--line);border-radius:6px;padding:1px 7px;background:var(--bg)}
.sid{font-family:"Cascadia Code",Consolas,monospace;font-size:12.5px;color:var(--accent);word-break:break-all}
.tmpl{font-size:11px;color:var(--faint);border:1px solid var(--line);border-radius:5px;padding:0 6px}
.metrics{margin-left:auto;font-size:12px;color:var(--faint);font-variant-numeric:tabular-nums;white-space:nowrap}
.stitle{font-size:13.5px;color:var(--soft);margin-bottom:9px}
.say{font-size:17.5px;line-height:1.82;margin:0 0 10px}

details.spoken{border-top:1px dashed var(--line);padding-top:8px;margin-top:4px}
details.spoken summary{cursor:pointer;color:var(--accent);font-size:12.5px;font-weight:600;
  list-style:none;user-select:none}
details.spoken summary::-webkit-details-marker{display:none}
details.spoken summary::before{content:"\\25B8 "}
details.spoken[open] summary::before{content:"\\25BE "}
.spk{background:var(--codebg);border-radius:8px;padding:12px 15px;margin:9px 0 4px;
  font-size:14.5px;line-height:1.75;color:var(--soft)}

.gap{background:var(--paper);border:1px solid var(--line);border-left:4px solid var(--hot);
  border-radius:10px;padding:16px 20px;margin:14px 0}
.gap-head{font-size:13px;margin-bottom:9px}
.gap-what{margin:0 0 11px;font-size:15.5px}
.tagx{display:inline-block;background:var(--hotsoft);border:1px solid var(--hotline);color:var(--hot);
  font-size:11px;font-weight:700;padding:1px 7px;border-radius:5px;margin-right:7px;vertical-align:2px}
.gap-row{margin:0 0 9px;font-size:14.5px;color:var(--soft)}
.gap-row:last-child{margin-bottom:0}
.gap-row b{color:var(--ink)}
.gap-row .k{display:block;font-size:11.5px;font-weight:700;letter-spacing:.05em;
  text-transform:uppercase;color:var(--faint);margin-bottom:2px}

.chg-list{display:flex;flex-direction:column;gap:11px}
.chg{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:14px 19px}
.chg-head{display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin-bottom:6px;font-size:13px}
.chg-tag{background:var(--accentsoft);border:1px solid var(--accentline);color:var(--accent);
  font-size:11.5px;font-weight:700;padding:1px 8px;border-radius:5px}
.chg p{margin:0;font-size:14.5px;color:var(--soft)}
.chg p b{color:var(--ink)}

.ask{background:var(--hotsoft);border:2px solid var(--hotline);border-radius:12px;
  padding:20px 24px;margin:46px 0 0}
.ask h2{margin:0 0 10px;font-size:19px;color:var(--hot)}
.ask ol{margin:0;padding-left:22px;font-size:16.5px}
.ask li{margin:7px 0}
.ask-note{margin:12px 0 0;font-size:13.5px;color:var(--soft)}

.foot{margin-top:40px;padding-top:14px;border-top:1px solid var(--line);
  color:var(--faint);font-size:12.5px;line-height:1.7}
mjx-container[jax="SVG"]{color:inherit}
""".strip()


if __name__ == "__main__":
    sys.exit(build())
