"""Build PLAN-act3-storyboard.html -- the Remotion pilot planning doc for §3.1 Act 3.

What it does (offline, no API):
  1. reads the LOCKED MiMo manifest + the rendered film's timeline.json from the MAIN checkout
     (video/output/ is gitignored, so a worktree does not have it);
  2. pulls representative frames out of the Manim film with ffmpeg (480 px JPEG q70) and
     embeds them as base64, so the HTML is one self-contained file;
  3. writes the HTML next to this script. Narration text and beat times come straight from
     the manifest (verbatim), never retyped here.

Usage (Git Bash, from anywhere):
    python video/experiments/remotion_pilot/build_plan.py [--film-dir <.../video/output/ch03/s3.1>]

Requires ffmpeg on PATH and Pillow (both already in ENVIRONMENT.md).
"""
from __future__ import annotations

import argparse
import base64
import html
import io
import json
import subprocess
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
OUT_HTML = HERE / "PLAN-act3-storyboard.html"
FPS = 30
THUMB_W = 480
JPEG_Q = 70

ACT_SCENES = ["intro", "divider_derivatives", "derivative_of_sine", "derivative_of_cosine",
              "slope_equals_height", "derivative_cycle", "outro"]


def main_checkout() -> Path:
    common = subprocess.run(["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
                            cwd=HERE, capture_output=True, text=True, check=True).stdout.strip()
    return Path(common).parent


# ----------------------------------------------------------------------------------------------
# frames: scene id -> list of scene-relative seconds (the clip clock, i.e. INCLUDING the 1.0 s
# lead). Picked after looking at a dense sampling of the film; each one shows a state the plan
# talks about (post-reveal state at a beat end, or a mid-animation state of a hook).
# ----------------------------------------------------------------------------------------------
FRAMES = {
    "intro": [1.5, 3.8, 6.2, 7.0, 9.4],
    "divider_derivatives": [3.0],
    "derivative_of_sine": [0.5, 5.1, 14.3, 15.1, 15.8, 24.3, 25.2, 31.9, 38.1],
    "derivative_of_cosine": [0.5, 6.4, 12.6, 15.1, 18.5, 19.4, 21.2, 22.2, 22.94, 33.1, 34.28,
                             40.7, 47.6],
    "slope_equals_height": [0.5, 5.2, 11.7, 17.6, 21.1, 23.8, 24.6, 26.6, 28.4, 34.1],
    "derivative_cycle": [0.5, 10.8, 11.4, 19.5, 23.0, 33.5],
    "outro": [1.6, 3.0, 5.5],
}


def grab(film: Path, t: float) -> str:
    png = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(film),
                          "-frames:v", "1", "-vf", f"scale={THUMB_W}:-1", "-f", "image2pipe",
                          "-vcodec", "png", "-"], capture_output=True, check=True).stdout
    im = Image.open(io.BytesIO(png)).convert("RGB")
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=JPEG_Q, optimize=True)
    return base64.b64encode(buf.getvalue()).decode("ascii")


# ----------------------------------------------------------------------------------------------
# prose (繁體中文). Math is MathJax \( \); `R` marks a SPEC-motion-language rule.
# ----------------------------------------------------------------------------------------------

def esc(s: str) -> str:
    return html.escape(s, quote=False)


def sw(hexv: str) -> str:
    return f'<span class="sw" style="background:{hexv}"></span><code>{hexv}</code>'


# ---------- Part A.1 colours --------------------------------------------------------------
COLOR_ROWS = [
    # (group, token, hex, used for in Act 3, source, remotion token, lock)
    ("深色教學底（DARK）", "bg", "#0a1322", "教學場與 divider 的底色（平塗，無漸層）", "theme.py:127", "color.dark.bg", "鎖死"),
    ("深色教學底（DARK）", "panel / card_fill", "#13233f", "卡片（accent_panel）底：定理 statement 卡、環節點卡", "theme.py:128,172", "color.dark.panel", "鎖死"),
    ("深色教學底（DARK）", "ink_1 / primary", "#eef2fb", "標題、statement、定理卡內式子、環節點式子、divider 標題", "theme.py:134,162", "color.dark.ink1", "鎖死"),
    ("深色教學底（DARK）", "ink_2 / text", "#c6cedd", "motive、證明列、草稿列、divider 副標與問題列、d/dx 標籤", "theme.py:134,168", "color.dark.ink2", "鎖死"),
    ("深色教學底（DARK）", "ink_3 / muted", "#6b748a", "PROOF 標、軸線、刻度與刻度字、環箭頭、虛線 connector、summit bars", "theme.py:134,169", "color.dark.ink3", "鎖死"),
    ("深色教學底（DARK）", "ink_faint", "#444c5e", "divider 進度點（非當前）", "theme.py:134", "color.dark.inkFaint", "鎖死"),
    ("深色教學底（DARK）", "hairline", "#22324f", "卡片描邊、spine 細線", "theme.py:156", "color.dark.hairline", "鎖死"),
    ("深色教學底（DARK）", "hairline_strong", "#33456a", "變動前框選（frame）、兩段式消去的框", "theme.py:156；derivation.py:266；hooks:1984", "color.dark.hairlineStrong", "鎖死"),
    ("卡片語意色（Direction B，對位講義 calcbook.sty）", "result", "#4fa6de", "accent: theorem → eyebrow「[ THEOREM ]」、statement 卡左條、spine cap", "theme.py:148；blocks.py:72-78", "role.result", "鎖死（場景只選 accent 名）"),
    ("卡片語意色（Direction B，對位講義 calcbook.sty）", "result_ink", "#79bfe8", "定理場 qed 拍的 indicate 閃色", "theme.py:153；scene.py:214", "role.resultInk", "鎖死"),
    ("卡片語意色（Direction B，對位講義 calcbook.sty）", "aside", "#96a0ae", "accent: remark 的 eyebrow／spine cap；無 accent 的 divider eyebrow 與進度 pill", "theme.py:152；blocks.py:92,100", "role.aside", "鎖死"),
    ("卡片語意色（Direction B，對位講義 calcbook.sty）", "aside_ink", "#b3bbc7", "remark 場 indicate 閃色（derivative_cycle）", "theme.py:154", "role.asideInk", "鎖死"),
    ("卡片語意色（Direction B，對位講義 calcbook.sty）", "concept / practice / caution / strategy", "#d98f3c", "本幕未出現（concept #d98f3c、practice #3ebe7c、caution #d96b6b、strategy #a493e6）；列出以示整組 token 一併移植", "theme.py:147-151", "role.*", "鎖死"),
    ("本節函數語意色（規則 5；實際上畫面用的是凍結別名）", "sin → accent", "#f2b13c", "sin 曲線與「y=sin x」標籤、環節點（sin x／−sin x）左條", "theme.py:164；storyboard color_role: accent；hooks:1251-1253", "deck.sin", "鎖死（deck 級）"),
    ("本節函數語意色（規則 5；實際上畫面用的是凍結別名）", "cos → secondary", "#5cc8ec", "cos 虛線曲線、cos 讀數點與標籤、環節點（cos x／−cos x）左條；也是 divider hero curve、intro 暗場 eyebrow 與 rule", "theme.py:163；hooks:640,762-763,1252-1254", "deck.cos", "鎖死（deck 級）"),
    ("本節函數語意色（規則 5；實際上畫面用的是凍結別名）", "斜率／結論 → success", "#54d199", "三條切線與 m= 標籤、QED 列「⇒ …」與 ■ 框", "theme.py:167；hooks:641；theorem_proof.py:152-163", "deck.slope", "鎖死（deck 級）"),
    ("本節函數語意色（規則 5；實際上畫面用的是凍結別名）", "θ → strategy", "#a493e6", "meta.color_map 唯一一條；本幕式子沒有 θ，不上畫面", "storyboard ch03_trig_derivatives.yml:48-49", "deck.colorMap['\\theta']", "鎖死（deck 級）"),
    ("本節函數語意色（規則 5；實際上畫面用的是凍結別名）", "amber_ink", "#e8ab63", "無 accent 場（slope_equals_height）的 indicate 與配對脈衝色", "theme.py:144；scene.py:214-215；hooks:806", "role.highlightInk", "鎖死"),
    ("米紙品牌底（LIGHT，片頭／片尾）", "bg", "#f4f1e9", "intro 前兩段、outro 底色", "theme.py:177", "color.paper.bg", "鎖死"),
    ("米紙品牌底（LIGHT，片頭／片尾）", "heading / brand_navy", "#16294e", "「Chapter 3」、節標題、outro 大標、outro summit bars", "theme.py:197,208", "color.paper.heading", "鎖死"),
    ("米紙品牌底（LIGHT，片頭／片尾）", "accent / brand_red", "#ba0c2f", "COURSE MAP、目前節點啟動點、END OF SECTION、outro rule、Next ▶、§3.2", "theme.py:196,202", "color.paper.brandRed", "鎖死"),
    ("米紙品牌底（LIGHT，片頭／片尾）", "subtitle / ink_3", "#767d8c", "章標題副行、「Next」", "theme.py:179,209", "color.paper.ink3", "鎖死"),
    ("米紙品牌底（LIGHT，片頭／片尾）", "ink_faint", "#aab0bd", "時間軸 rail 與節點", "theme.py:179", "color.paper.inkFaint", "鎖死"),
    ("米紙品牌底（LIGHT，片頭／片尾）", "text / ink_2", "#444b59", "outro「The Chain Rule」", "theme.py:179,206", "color.paper.ink2", "鎖死"),
]

GLOW_NOTE = (r"光暈（glow）：函數曲線＝同色描邊 12（manim stroke 單位）、不透明度 0.24 墊在 5 寬實線下"
             r"（graph.py:478）；divider hero curve＝glow_curve，halo 寬＝實線×2.7（theme.py:222）、不透明度 0.22（brand.py:782-792）。"
             r"Remotion 用同樣的「雙描邊」SVG 疊法即可像素貼近；若改 CSS <code>filter: blur()</code> 真光暈會更柔，但屬外觀改動（見 Part C-8）。")

# ---------- Part A.2 type -----------------------------------------------------------------
TYPE_SCALE = [
    # token, px, used for
    ("h1", 78, "場標題（theorem／definition 版）；graph 標題為 0.88×h1≈69"),
    ("intro_headline", 92, "divider 標題"),
    ("outro_headline", 78, "outro 節標題"),
    ("h2", 58, "intro 課程地圖「Chapter 3」"),
    ("statement", 44, "定理 statement、definition statement"),
    ("step / body", 42, "證明列（數學）、qed 列"),
    ("prose_sm", 38, "motive（scaffold）"),
    ("intro_subtitle", 35, "divider 副標、intro 標語、章標題副行"),
    ("caption / label", 30, "刻度字、m=／cos 讀數標籤、outro Next 行"),
    ("eyebrow", 26, "「[ THEOREM ]」「STAGE 3」「PROOF」（mono，全大寫）"),
    ("ghost_numeral", 520, "divider 背景大數字（5% 不透明）"),
]
MATH_TIERS = [("math_conclusion", 62), ("math", 48), ("step（證明列）", 42), ("statement", 44),
              ("math_rail（草稿、環節點、d/dx、軸標 x/y）", 34), ("label（刻度、讀數）", 30)]

# ---------- Part B scene content ----------------------------------------------------------
# For content scenes: beat index (manifest 1-based; 0 = the 1.0 s lead) -> dict.
SCENES: dict[str, dict] = {}

SCENES["intro"] = dict(
    template="<code>intro</code> 模板（<code>templates/intro.py</code>＋<code>scene._play_intro</code>）",
    remotion="<code>&lt;IntroGate&gt;</code>（三段 <code>&lt;Sequence&gt;</code>：品牌開場 → 課程地圖 → 暗場交接）",
    audio="無旁白；house cue＝<code>candidate_b_intro_bed.wav</code>（gain 1.0、尾端淡出 0.6 s；house_audio.py:46）",
    stages=[
        ("0.0–1.0", "lead：空白米紙（片頭由黑 0.2 s 淡入）。"),
        ("≈1.0–2.1", "NTU logo lockup 置中淡入（0.5 s）後停住。"),
        ("≈2.1–2.9", "logo 下移 0.05u 淡出（0.65 s）。"),
        ("≈2.9–4.4", "「COURSE MAP」（品牌紅 mono）＋「Chapter 3」（海軍藍粗體）＋章名（灰）淡入；右下 summit bars 淡入；左側 rail 與 3.1／3.2／3.3 節點淡入。"),
        ("≈4.7–5.2", "目前節點 3.1 的點由灰轉品牌紅（0.5 s）。3.1 在最上面，所以沒有 pulse 線段。"),
        ("≈5.4–6.2", "節名「Derivatives of the Sine and Cosine Functions」以 Create 逐字寫出（0.8 s）。"),
        ("≈6.8–7.8", "米紙 → 深海軍藍 crossfade 1.0 s（課程地圖同時下移淡出）。"),
        ("≈7.8–9.0", "暗場標記淡入：「SECTION 3.1」（青藍 mono）、白色粗體節標題、青藍短 rule、標語「How fast does sine change?」；右下 summit bars。"),
        ("≈9.0–10.3", "停住＋ tail 1.0 s，0.2 s 淡黑出場。"),
    ],
    frames_note="幀（場內秒）：1.5 logo／3.8 地圖標頭／6.2 節名寫完／7.0 crossfade 中／9.4 暗場標記",
    remotion_body=(
        "三段全部照搬，時間點不用 manim 的「動畫總和」推算，而是 Part D 從 film 量出每段起點的幀號寫成 "
        "<code>INTRO_STAGES</code> 常數（code 推算合計 10.44 s，film 實為 10.3 s，差 0.14 s，所以一定要量，不能算）。"
        "logo 用 <code>pipeline/assets/lockup-color-outlined.svg</code> 原檔（<code>&lt;Img&gt;</code>），"
        "節名逐字寫＝逐字 clip 擦出；crossfade＝兩層 <code>AbsoluteFill</code> 的 opacity interpolate。"
    ),
    proposals=[],
)

SCENES["divider_derivatives"] = dict(
    template="<code>divider</code> 模板（<code>templates/divider.py</code>＋<code>scene._play_timed</code>）",
    remotion="<code>&lt;Divider&gt;</code>",
    audio="無旁白；house cue＝<code>candidate_b_divider_stinger.wav</code>（gain 0.6、淡出 0.4 s；house_audio.py:48）",
    stages=[
        ("0.0–6.0", "整幅一次到位（所有 block 都是 static，連 hero curve 的 <code>create</code> 也不播），只靠邊界 0.2 s 淡黑進出；中間 5.6 s 是全靜止。"
                    "畫面：右側 5% 白的巨大「3」；青藍 glow 曲線由左下掃到右上並出血；左側垂直置中一疊——「STAGE 3」（slate mono）、"
                    "「The Two Derivatives」（白粗體 92）、問題列 \\(\\dfrac{d}{dx}\\sin x=\\;?\\quad\\dfrac{d}{dx}\\cos x=\\;?\\)（ink_2）、"
                    "「Assembling the pieces.」（ink_2）、4 顆進度點第 3 顆為 slate pill；右下 summit bars。"),
    ],
    frames_note="幀（場內秒）：3.0（整場同一張）",
    remotion_body="版面、字級、色全部走 tokens；props＝eyebrow／title／subtitle／scaffold.problem／ghost／progress，直接讀 storyboard。",
    proposals=[
        ("D1", "hero curve 用 <code>evolvePath</code> 在前 0.8 s 畫出來，左側一疊以 0.25 s 間隔依序淡入（即 manim <code>_play_timed</code> 原本的 gap），總長仍 6.0 s。", "規則 2（曲線畫出來）；divider 是品牌幀，規則 4 不強制，屬加分。"),
        ("D2", "問題列 \\(\\dfrac{d}{dx}\\sin x=\\;?\\) 在場尾不淡黑，直接帶進下一場當 statement 的前身（見 derivative_of_sine 的 S1）。", "規則 1（一場一張畫布／carry）。"),
    ],
)

SCENES["derivative_of_sine"] = dict(
    template="<code>theorem_proof</code>，accent: theorem（→ role result 藍），6 beats，<code>scene_aligned</code>",
    remotion="<code>&lt;TheoremProof&gt;</code>（無 hook）",
    audio="<code>audio_mimo/scenes/15_derivative_of_sine.wav</code>（37.417 s）",
    beats={
        0: dict(frames=[0.5], manim="開場幀（static）：左上「[ THEOREM ]」藍 mono、白粗體標題、motive「Cash in continuity…」（ink_2）；左側 spine 細線＋藍 cap；右下 summit bars。body 全空。",
                remotion="<code>SceneShell</code>＋<code>Masthead</code>，第 0 幀即完整。", rule="—"),
        1: dict(frames=[], manim="沒有 reveal，畫面不變。從場開頭算起 body 已空了 4.5 s（未達 6 s）。",
                remotion="同 Manim。", rule="規則 4（4.5 s < 6 s，合格）",
                improve=[("S1", "【需 D2】divider 的問題列 \\(\\tfrac{d}{dx}\\sin x=\\;?\\) 硬切帶進來，0.8 s 飛到右上 statement 卡的位置、縮到 statement 字級，body 不再空白。")]),
        2: dict(frames=[5.1], manim="statement 卡從左 slide 進右上 rail（0.5 s，右移 47 px）：panel 底、細描邊、5 px 藍左條，內容 \\(\\frac{d}{dx}\\sin x=\\cos x\\)（44，ink_1）。之後靜止 4.8 s。",
                remotion="<code>&lt;Reveal kind=\"slide\"&gt;&lt;Card variant=\"rail\" bar=\"result\"&gt;&lt;MathTex size=\"statement\"/&gt;</code>。",
                rule="規則 2",
                improve=[("S1（續）", "採 S1 時改成 token morph：「?」原位變成 \\(\\cos x\\)，卡框在字後長出——旁白「is cosine x」正落在這個 token 上。")]),
        3: dict(frames=[14.3], manim="「PROOF」小標（muted mono）隨 proof.0 先淡入（0.5 s），再淡入 proof.0：\\(\\frac{d}{dx}\\sin x=\\lim_{h\\to0}\\frac{\\sin(x+h)-\\sin x}{h}\\)（ink_2）。靜止約 3.8 s。",
                remotion="<code>&lt;Reveal kind=\"fade\"&gt;</code>×2 依序；MathTex 帶 <code>{{…}}</code> 分段 id。", rule="規則 2（首列整塊淡入 1 次，合格）"),
        4: dict(frames=[15.1, 15.8, 24.3], manim="先在 proof.0 外畫 hairline 框（0.4 s），再 TransformMatchingShapes 1.2 s：proof.0 的字形複本飛下去組成 proof.1 \\(=\\lim_{h\\to0}\\cos\\!\\left(x+\\frac h2\\right)\\frac{\\sin(h/2)}{h/2}\\)，proof.0 退到 55% 不透明、框同時淡出。中間幀（15.8）字形糊成一團。變完後靜止 8.4 s。",
                remotion="<code>&lt;FrameBox target=\"proof.0\"/&gt;</code>（12f）→ <code>&lt;TokenMorph from=\"proof.0\" to=\"proof.1\"/&gt;</code>（36f，同名分段平移／縮放，不同名的交叉淡入淡出）＋ <code>&lt;Dim to={0.55}/&gt;</code>。",
                rule="規則 2、3", still="未宣告長靜止 8.4 s",
                improve=[("S2", "隨旁白點名做分段強調：唸到「cosine of the quantity x plus one half h」時 \\(\\cos(x+\\frac h2)\\) 段短暫 indicate，唸到「sine of h over two, all over h over two」時分式段 indicate。時間取自 <code>align/15_derivative_of_sine.words.json</code>（離線檔，已存在）。不加任何新字。")]),
        5: dict(frames=[25.2, 31.9], manim="TransformMatchingShapes 1.2 s：proof.1 變出 proof.2 \\(\\cos\\!\\left(x+\\frac h2\\right)\\to\\cos x,\\quad\\frac{\\sin(h/2)}{h/2}\\to1\\)，proof.1 退 55%。之後靜止 6.4 s。",
                remotion="<code>&lt;TokenMorph&gt;</code>：兩個同名段（cos 因子、分式）平移到新位置，「\\(\\to\\cos x\\)」「\\(\\to1\\)」淡入。",
                rule="規則 2", still="未宣告長靜止 6.4 s",
                improve=[("S3", "兩個極限錯開：「the first factor tends to cosine x」時只動第一段、「the second to one」時才動第二段（word timing）。最終幀與 Manim 相同。")]),
        6: dict(frames=[38.1], manim="綠色 qed 列「\\(\\Rightarrow\\ \\cos x\\cdot1=\\cos x\\)」＋綠框 ■ 淡入（0.5 s），接著 indicate statement 卡（result_ink 染色、放大 1.15、0.8 s）。之後靜止 4.9 s＋tail 1.0 s。",
                remotion="<code>&lt;Reveal kind=\"fade\"&gt;</code> → <code>&lt;Indicate target=\"statement\" color=\"resultInk\"/&gt;</code>（24f，there-and-back）。",
                rule="規則 3",
                improve=[("C 串①", "tail 1.0 s 內 statement 卡複本縮到 0.6 倍飛向右下，成為下一場的常駐提醒（見 C 串）。")]),
    },
)

SCENES["derivative_of_cosine"] = dict(
    template="<code>theorem_proof</code>＋hook <code>cosine_identity_draft</code>，accent: theorem，6 beats，<code>beats</code> 模式（逐拍 WAV，manifest 無 forced-alignment 區塊）",
    remotion="<code>&lt;TheoremProof&gt;</code>＋<code>&lt;CosineIdentityDraft&gt;</code>（hook 元件，包在 proof.0 的 reveal 外）",
    audio="<code>audio_mimo/scenes/17_derivative_of_cosine.wav</code>（46.88 s；逐拍檔在 <code>beats/17_derivative_of_cosine/</code>）",
    beats={
        0: dict(frames=[0.5], manim="開場幀同 sine 場（標題「The Derivative of Cosine」、motive「Same machinery, companion identity — now cosine.」）。",
                remotion="同 sine 場。", rule="—"),
        1: dict(frames=[], manim="無 reveal。自場開頭起 body 空 5.96 s（貼著 6 s 線）。", remotion="同 Manim。", rule="規則 4（邊緣）",
                improve=[("C 串②", "採 C 串時 sine 的定理卡已停在右側，body 不再空。")]),
        2: dict(frames=[6.4], manim="statement 卡 slide 進右上：\\(\\frac{d}{dx}\\cos x=-\\sin x\\)。靜止 4.1 s。", remotion="同 sine 場 beat 2。", rule="規則 2"),
        3: dict(frames=[12.6, 15.1, 18.5, 19.4, 21.2, 22.2],
                manim="PROOF＋proof.0 \\(\\cos A-\\cos B=-2\\sin\\frac{A+B}{2}\\,\\sin\\frac{A-B}{2}\\) 淡入；接著 hook 在 proof.1／proof.2 尚空的位置演草稿（math_rail，ink_2），切點是本拍時長的固定比例："
                       "≈+3.6 s 淡入 \\(u=\\frac{A+B}{2},\\ v=\\frac{A-B}{2}\\)；≈+5.5 s Write \\(\\cos(u+v)-\\cos(u-v)\\)；≈+6.8 s 變形為展開式 \\((\\cos u\\cos v-\\sin u\\sin v)-(\\cos u\\cos v+\\sin u\\sin v)\\)；"
                       "≈+8.3 s 兩個 \\(\\cos u\\cos v\\) 加框→轉灰→消失（兩段式消去）；≈+9.3 s 殘項合攏成 \\(-2\\sin u\\sin v\\)、代換列淡出；≈+10.0 s 複本飛上 proof.0 右側；≈+10.8 s 清空草稿帶。本拍無長靜止。",
                remotion="<code>&lt;CosineIdentityDraft cues={C_CUE}&gt;</code>：沿用 hook 的七個比例切點（hooks:1903-1911）換算成幀；展開與合攏用 <code>&lt;TokenMorph&gt;</code>，消去用 <code>&lt;CancelTwoStage&gt;</code>（框 12f → 轉灰 8f → 淡出 8f → 合攏）。",
                rule="規則 1、2、4",
                improve=[("M1", "（全片通用）morph 改走分段平移，不做字形重組，中間幀不會像 Manim 那樣糊成一團；起點與終點幀不變。")]),
        4: dict(frames=[22.94, 33.1], manim="框 proof.0（0.4 s）→ 1.2 s 變形出 proof.1 \\(\\frac{\\cos(x+h)-\\cos x}{h}=-\\sin\\!\\left(x+\\frac h2\\right)\\frac{\\sin(h/2)}{h/2}\\)，proof.0 退 55%。之後靜止 9.4 s。",
                remotion="同 sine 場 beat 4。", rule="規則 2、3", still="未宣告長靜止 9.4 s（本幕最長）",
                improve=[("K2", "同 S2：「difference quotient」→ 左邊分式段、「negative sine of the quantity x plus one half h」→ 第二段、「sine of h over two…」→ 分式段依序 indicate。本場沒有 words.json，需先用本機 stable-ts（不計費）對 <code>beats/17_derivative_of_cosine/04_*.wav</code> 做對齊，或沿用比例切點。")]),
        5: dict(frames=[34.28, 40.7], manim="1.2 s 變形出 proof.2 \\(-\\sin\\!\\left(x+\\frac h2\\right)\\to-\\sin x,\\quad\\frac{\\sin(h/2)}{h/2}\\to1\\)。之後靜止 6.3 s。",
                remotion="同 sine 場 beat 5。", rule="規則 2", still="未宣告長靜止 6.3 s",
                improve=[("K3", "同 S3，兩個極限隨「the sine factor…」「the second to one」錯開。")]),
        6: dict(frames=[47.6], manim="綠色 qed「\\(\\Rightarrow\\ -\\sin x\\cdot1=-\\sin x\\)」■ 淡入 → indicate statement。之後靜止 5.6 s＋tail 1.0 s。",
                remotion="同 sine 場 beat 6。", rule="規則 3", still="含 tail 共 6.6 s（旁白講完後才過 6 s）",
                improve=[("C 串③", "tail 內兩張定理卡（sin、cos）一起縮小飛到右上角，準備帶進圖形場。")]),
    },
)

SCENES["slope_equals_height"] = dict(
    template="<code>graph</code> single＋hook <code>slope_equals_height</code>，無 accent（spine cap 為中性灰、沒有 eyebrow），7 beats，<code>scene_aligned</code>",
    remotion="<code>&lt;Graph&gt;</code>＋<code>&lt;SlopeEqualsHeight&gt;</code>（hook 元件：切線、刻度、配對讀數）",
    audio="<code>audio_mimo/scenes/17_slope_equals_height.wav</code>（33.44 s）",
    beats={
        0: dict(frames=[0.5], manim="開場幀（static）：白粗體標題「Slope Equals Height」（0.88×h1、無 eyebrow）、灰色座標軸（帶箭頭與 x／y）、刻度字 0、\\(\\tfrac{\\pi}{2}\\)、\\(\\pi\\)；右下 summit bars。",
                remotion="<code>&lt;Axes&gt;</code>（SVG line＋tip），尺寸照 storyboard <code>axes</code>（x_length 8.6u、y_length 4.7u）並跑同一個 fit-to-zone。", rule="—"),
        1: dict(frames=[], manim="無 reveal，只有軸，場開頭起 4.1 s 不動。", remotion="同 Manim。", rule="規則 4（4.1 s，合格）",
                improve=[("C 串④", "兩張定理卡停在右上角；旁白「that theorem」時 \\(\\frac{d}{dx}\\sin x=\\cos x\\) 那張 indicate。")]),
        2: dict(frames=[5.2], manim="sin 曲線 Create 0.8 s（琥珀實線＋同色光暈），標籤「\\(y=\\sin x\\)」同色。靜止 4.0 s。",
                remotion="<code>&lt;FunctionPlot fn=\"sin\" color=\"deck.sin\" draw/&gt;</code>，用 <code>@remotion/paths</code> 的 <code>evolvePath</code> 畫出。", rule="規則 2、5"),
        3: dict(frames=[11.7], manim="x=0 的綠切線 Create 0.65 s＋「m=1」（沿切線法向偏移）。", remotion="<code>&lt;Tangent x={0} slope={1}/&gt;</code>。", rule="規則 2、5"),
        4: dict(frames=[17.6], manim="x=π/2 的水平切線＋「m=0」。靜止 5.3 s。", remotion="同上。", rule="規則 2",
                improve=[("G2", "切線滑行：beat 4 開頭從 x=0 那條切線複製一條沿 sin 滑到 π/2，途中 m 讀數連續變化，停下時與 Manim 的 m=0 切線重合；beat 5 同理滑到 π。三條最終切線不變。")]),
        5: dict(frames=[21.1], manim="x=π 的切線＋「m=−1」。", remotion="同上。", rule="規則 2"),
        6: dict(frames=[23.8], manim="cos 虛線曲線 Create 0.8 s（青藍）＋標籤「\\(y=\\cos x\\)」在曲線下方。", remotion="<code>&lt;FunctionPlot fn=\"cos\" dashed color=\"deck.cos\"/&gt;</code>（stroke-dasharray）。", rule="規則 2、5"),
        7: dict(frames=[24.6, 26.6, 28.4, 34.1],
                manim="三次配對，每次 1.2 s：虛線 connector 由 sin 上的點往下畫到 cos（0.35 s）→ 青藍讀數點與「\\(\\cos0=1\\)」等標籤落地（0.25 s）→ 切線與讀數點同時以 amber_ink 脈衝（0.6 s）。三次後 indicate 三條切線（0.8 s）。之後靜止約 6.0 s＋tail 1.0 s。",
                remotion="<code>&lt;PairReadoff pairs={3} perSeconds={1.2}/&gt;</code>，比例 0.29／0.21／0.50 照搬（hooks:797-798）。",
                rule="規則 3、5", still="未宣告長靜止約 6.0 s（再加 tail 共約 7 s）",
                improve=[("G3", "配對完後做連續 sweep：x 由 0 走到 π（約 4 s），綠切線沿 sin 滑、即時顯示 m；同一個 x 上青藍點沿 cos 走、虛線 connector 跟著——每個 x 上斜率都等於高度，正是「the slope of sine is the height of cosine, the theorem drawn」。sweep 物件在場尾前淡出，最終幀回到三組配對。")]),
    },
)

SCENES["derivative_cycle"] = dict(
    template="<code>definition_math</code>＋hook <code>derivative_cycle</code>（把 math.0 換成四節點環），accent: remark（→ aside slate），4 beats，<code>paced: [math.1]</code>",
    remotion="<code>&lt;DefinitionMath&gt;</code>＋<code>&lt;DerivativeCycleRing&gt;</code>",
    audio="<code>audio_mimo/scenes/18_derivative_cycle.wav</code>（32.8 s）",
    beats={
        0: dict(frames=[0.5], manim="開場幀：「[ REMARK ]」slate mono、標題「The Derivative Cycle」、motive「Step back: what pattern…」。body 空。",
                remotion="<code>SceneShell accent=\"remark\"</code>。", rule="—"),
        1: dict(frames=[], manim="無 reveal，場開頭起 4.4 s 不動。", remotion="同 Manim。", rule="規則 4（合格）"),
        2: dict(frames=[10.8], manim="statement 兩行 prose（44，ink_1）slide 進來：「Differentiation cycles sine and cosine, with a sign flip every / second step.」。之後靜止 6.3 s。",
                remotion="<code>&lt;Reveal kind=\"slide\"&gt;</code>；斷行寫死在 props（瀏覽器依實際字寬斷行，可能與 LaTeX 不同）。",
                rule="規則 2", still="未宣告長靜止 6.3 s",
                improve=[("Y1", "statement 改逐字寫入、跨整拍（等同 storyboard 對它加 <code>paced</code>），寫完留 0.6 s。")]),
        3: dict(frames=[11.4, 19.5], manim="整個環一次 Write（0.8 s）：四張節點小卡（math_rail，左條 sin 系琥珀／cos 系青藍交替）位於寬矩形四角，四支灰箭頭沿周邊順時針，中央「\\(\\frac{d}{dx}\\)」（ink_2）。之後靜止 7.9 s。",
                remotion="<code>&lt;DerivativeCycleRing&gt;</code>：節點＝<code>&lt;Card variant=\"node\"&gt;</code>，箭頭＝SVG path＋tip。",
                rule="規則 2、5", still="未宣告長靜止 7.9 s",
                improve=[("Y2", "照旁白順序長環：「sine x」節點 →（箭頭畫出）「cosine x」→「negative sine x」→「negative cosine x」→「and back to sine x」時最後一支箭頭閉環；「Writing an arrow for one derivative」時中央 d/dx 出現。時間取自 <code>align/18_derivative_cycle.words.json</code>。"),
                         ("C 串⑤", "兩張帶進來的定理卡變形成環的前兩條邊（sin→cos、cos→−sin），其餘兩條由規律補上。")]),
        4: dict(frames=[23.0, 33.5], manim="math.1 \\(\\dfrac{d^{4}}{dx^{4}}\\sin x=\\sin x\\qquad\\text{vs.}\\qquad\\dfrac{d}{dx}e^{x}=e^{x}\\) 隨旁白逐段寫滿整拍（paced，約 12.6 s）；最後 indicate 整個環（aside_ink、0.8 s）。本拍無長靜止。",
                remotion="<code>&lt;PacedWrite segments=…/&gt;</code>（逐段淡入＋左→右 clip）→ <code>&lt;Indicate target=\"math.0\" color=\"asideInk\"/&gt;</code>。",
                rule="規則 2、3、4",
                improve=[("Y3", "把最後的整環閃爍換成「繞一圈」：亮點沿 sin→cos→−sin→−cos→sin 走四步回到起點，對上「Four derivatives and you are home」。")]),
    },
)

SCENES["outro"] = dict(
    template="<code>outro</code> 模板（<code>templates/outro.py</code>＋<code>scene._play_outro</code>）",
    remotion="<code>&lt;Outro&gt;</code>",
    audio="無旁白；house cue＝<code>candidate_b_outro_bed.wav</code>（gain 1.0、淡出 0.8 s；house_audio.py:47）",
    stages=[
        ("0.0–1.0", "lead：米紙＋右下海軍藍 summit bars（static），由黑 0.2 s 淡入。"),
        ("≈1.0–4.0", "依序淡入（每件 0.5 s＋0.12 s 間隔）：NTU logo → 品牌紅短 rule → 「END OF SECTION 3.1」（紅 mono）→ 節標題（海軍藍粗體 78）→「▶ Next §3.2 The Chain Rule」。"),
        ("≈4.0–7.0", "停住 2 s＋tail，片尾 0.2 s 淡黑。"),
    ],
    frames_note="幀（場內秒）：1.6 logo／3.0 標題淡入中／5.5 完成",
    remotion_body="全照搬；<code>next_section</code>／<code>next_title</code> 讀 storyboard。",
    proposals=[],
)

C_CHAIN = (
    "<b>C 串（跨場 carry，一個提案、五個落點）</b>：S1（divider 問題列 → sine 的 statement）＋①（sine 定理卡場尾縮到角落）＋②（cosine 場中常駐）＋③（兩卡一起飛到右上）＋④（圖形場「that theorem」時閃）＋⑤（在環場變成前兩條邊）。"
    "目的是讓規則 1「一幕一張畫布」在本幕真的成立：兩條定理從被證明、被畫成圖、到被收成循環，是<em>同一個物件</em>一路被帶著走。"
    "代價：C 串涉及的邊界改硬切（不淡黑），各場單獨預覽時要以 <code>carriedIn</code> prop 模擬前一場帶進來的物件。"
)

# ---------- Part C decisions --------------------------------------------------------------
DECISIONS = [
    ("外觀基準", "第一版要「像素貼近 Manim」還是允許翻新？",
     "兩版並行：<b>A 版</b>貼近 Manim（驗證 tokens 與同步都搬對了），<b>B 版</b>＝A 版＋你在第 10 條點頭的改良提案（以 zod prop <code>improvements</code> 開關，不另寫一套）。"),
    ("函數色", "沿用 film 實際的凍結別名（sin <code>#f2b13c</code>／cos <code>#5cc8ec</code>／綠 <code>#54d199</code>），還是改用 Direction B 色相（<code>#d98f3c</code>／<code>#4fa6de</code>／<code>#3ebe7c</code>）？theme.py 註明這是未決的 D2-07。",
     "pilot 用凍結值，才能逐幀比。D2-07 另案決定，兩條產線一起改。"),
    ("數學字型", "MathJax 4＋<code>mathjax-newcm</code>（New Computer Modern，與 Latin Modern 同出 Computer Modern）、MathJax 3 預設 TeX 字型，還是 KaTeX？",
     "MathJax 4＋newcm、SVG 輸出。字形最接近 lmodern，也能用 <code>\\class{}</code> 標分段、做 token morph。"),
    ("數學排版時機", "建置前預先把 TeX 轉成 SVG（Node 腳本），還是 render 時由 MathJax 現排（<code>delayRender</code>）？",
     "預先轉。結果固定、render 快，分段邊界框也能先量好給 TokenMorph 用。"),
    ("解析度／幀率", "pilot 用 1920×1080＠30（與 film 相同），還是直接做 storyboard meta 寫的 4K60？",
     "pilot 用 1080p30，才能逐幀比對。4K60 等 A 版過關後改 composition fps＝60、render 時 <code>--scale=2</code>。所有時間都以秒寫、執行時換算幀數，換 fps 不用改 code。"),
    ("場間轉場", "保留每個邊界各 0.2 s 的淡黑、幕內 content→content 改硬切，還是交叉溶接？",
     "A 版保留淡黑，而且要用場內的邊緣淡黑 overlay 做，不能用 <code>TransitionSeries</code> 的 fade：後者兩場會重疊，時間軸變短，就對不上 film。B 版只在 C 串經過的邊界改硬切。"),
    ("「書寫」效果", "仿 manim Write（SVG 描邊再填色），左→右 clip 擦出，還是逐 token 淡入加輕微上移？",
     "數學用逐 token 淡入加上移，字形不會破；標題與節名文字用 clip 擦出。中間幀本來就不可能跟 Manim 一模一樣，只要求起點與終點幀一致。"),
    ("光暈", "用雙描邊模擬（與 Manim 相同），還是 CSS blur 做真光暈？", "A 版用雙描邊，blur 只當 B 版選項。"),
    ("音訊來源", "pilot 直接截 film 的最終混音（旁白、house cue、loudnorm 都已完成），還是用逐場 WAV 加 cue 重混？",
     "pilot 截 film 音軌，並排比較時兩邊聲音完全一樣。正式化時才改 <code>&lt;Audio&gt;</code> 逐場掛 WAV 加 cue，再比照 make.py 做 loudnorm。"),
    ("改良提案逐條", "D1、D2+S1、S2／K2、S3／K3、M1、C 串、G2、G3、Y1、Y2、Y3，各要不要？",
     "建議要：M1、S2／K2、S3／K3、G3、Y2（都在填「長靜止」，不加新字，最終幀不變）。建議要，但請你先看過：C 串（改動最大、最有 3B1B 味）、Y1、Y3。可有可無：D1、G2（G2 跟 G3 選一個就好，G3 較完整）。"),
    ("Remotion 授權", "Remotion 用自訂授權：據我所知，個人、3 人以下公司、非營利可免費，其他要買 Company License，請以 remotion.dev/license 為準。本計畫屬於哪一類？",
     "動工前請你確認；我判定不了。"),
    ("安裝", "pilot 需要在 <code>video/experiments/remotion_pilot/</code> 建 Node 專案，並安裝 <code>remotion</code>、<code>@remotion/cli</code>、<code>@remotion/paths</code>、<code>@remotion/fonts</code>、<code>@remotion/media</code>、<code>@remotion/transitions</code>、<code>zod</code>、<code>@mathjax/src</code>、<code>@mathjax/mathjax-newcm-font</code>。",
     "依 CLAUDE.md，要先經你同意才裝；裝完一併更新 ENVIRONMENT.md 與 doctor.py（標成實驗線，不列入必要環境）。"),
]

# ---------- Part D ------------------------------------------------------------------------
PART_D = r"""
<h3>D.1 檔案與資料夾（全部在 <code>video/experiments/remotion_pilot/</code>，不動產線）</h3>
<pre>
remotion_pilot/
  PLAN-act3-storyboard.html   ← 本檔；build_plan.py 重生
  README.md                   ← 動工時寫（繁中）：怎麼跑、怎麼比、已知差異
  package.json  remotion.config.ts  tsconfig.json
  scripts/
    export_act.py     storyboard（_mimo.yml）＋manifest＋timeline.json → src/data/act3.json
    tex2svg.mjs       act3.json 內所有 TeX → MathJax 4 SVG（含 {{…}} 分段框）→ src/data/math.json
    compare.py        切 film 對應段、並排、幀數與 reveal onset 比對、產 REVIEW html
  public/             （媒體不進 git）fonts/（複製 vendored Instrument Sans OTF＋Plex Mono）、
                      brand/lockup-color-outlined.svg、audio/act3_film.wav
  src/
    Root.tsx          &lt;Folder&gt; 放七個場的 connected composition ＋ Act3 總 composition
    Act3.tsx          &lt;Series&gt;；calculateMetadata 由 act3.json 加總幀數
    schema.ts         zod：scene spec、beats、improvements 開關
    theme/tokens.ts   Part A 全部 token（色、字級、版面、動作）
    components/       SceneShell Masthead Card MathTex Reveal Dim Indicate FrameBox TokenMorph
                      CancelTwoStage PacedWrite BeatTimeline Axes FunctionPlot Tangent
    templates/        IntroGate Divider Outro TheoremProof Graph DefinitionMath
    hooks/            CosineIdentityDraft SlopeEqualsHeight DerivativeCycleRing
  out/                （gitignore）
</pre>
<h3>D.2 資料流（誰讀什麼）</h3>
<ul>
<li><b><code>export_act.py</code>（Python，import 既有 pipeline）</b>：讀 <code>video/storyboards/ch03_trig_derivatives_mimo.yml</code>（film 實際用的衍生稿）的七個場，用 pipeline 自己的 <code>parse_say</code> 取 reveal 順序；讀 main checkout 的 <code>audio_mimo/manifest.json</code>，並先過 <code>pipeline.pauses.apply_pauses_timing</code>（本幕沒有 <code>pauses:</code>，照樣過，免得日後漏）；讀 <code>ch03_trig_derivatives_mimo.timeline.json</code> 取每場在 film 的起訖。輸出每場 <code>durationInFrames</code>（直接用 film 的幀數）與每拍 <code>fromFrame = round((1.0 + start_seconds)·fps)</code>。這些是唯一的時間來源，TSX 裡不准手寫秒數。</li>
<li><b><code>tex2svg.mjs</code></b>：把 <code>{{…}}</code> 轉成 <code>\class{seg-k}{…}</code>，<code>\everymath{\displaystyle}</code> 則以 display 模式排版對應；輸出 path 與各分段邊界框。</li>
<li><b>TSX</b>：<code>&lt;BeatTimeline&gt;</code> 把 act3.json 放進 context，模板用 <code>useBeat('proof.1')</code> 取 <code>{from, duration}</code>，每個 reveal 包成 <code>&lt;Sequence from&gt;</code>；動畫一律 <code>useCurrentFrame()</code>＋<code>interpolate()</code>（不用 CSS transition）。拍內順序照 scene.py：dim → rider → reveal → indicate。</li>
</ul>
<h3>D.3 校準（先做，決定 A 版能不能像素貼近）</h3>
<ol>
<li><b>文字字級</b>：Manim 的 px token 是「大寫高」校準值：cap height ≈ 0.894 × token px（theme.py:65-72；film 實測 h1 78 → 「T」高 68–69 px）。Instrument Sans capHeight＝0.72 em，所以 <b>CSS font-size ≈ 1.242 × token</b>（h1 78 → 96.9 px）。Plex Mono 的 eyebrow 要另外量。</li>
<li><b>數學字級</b>：film 實測 step 42 的證明列裡「cos」x-height ≈ 19 px；Latin Modern x-height 0.431 em，所以 em ≈ 44 px，<b>≈ 1.05 × token</b>。用 MathJax 排同一列再比 x-height，把常數寫進 tokens。</li>
<li><b>描邊寬</b>：manim stroke 單位 ≈ 1.35 px＠1080p（推估，待量）。軸 2 → 2.7 px、曲線 5 → 6.75 px、光暈 12 → 16 px。</li>
<li><b>緩動</b>：manim 預設 <code>smooth</code> 先以 <code>Easing.bezier(0.45,0,0.55,1)</code> 近似，再抽 film 某次 fade 的逐幀 opacity 擬合；Indicate 用 there-and-back。</li>
<li><b>粗體字距</b>：LaTeX 端把 Bold 的字間距補到 0.2101 em（_bootstrap.py:91-102）；瀏覽器用字型自帶的 space，差多少用 <code>word-spacing</code> 補，量標題寬度對齊。</li>
</ol>
<h3>D.4 同步驗證（對 film，逐場 ≤ 2 幀）</h3>
<ol>
<li><b>靜態檢查（0 誤差）</b>：每場 <code>durationInFrames</code> 等於 film 的場長幀數（intro 309、divider 180、sine 1182、cosine 1466、slope 1063、cycle 1043、outro 210，合計 5453 幀＝181.77 s）。每拍 <code>from</code> 等於同一公式算出的 Manim beat onset。</li>
<li><b>動態檢查（≤ 2 幀，比照 <code>timing.SYNC_HARD_GATE_FRAMES = 2</code>）</b>：<code>compare.py</code> 對兩支片逐幀做差分，找出每拍開始後第一個畫面變化（reveal onset）的幀號，逐拍比 |Δ|。改良提案（B 版）不在此列，只驗 A 版。</li>
<li><b>靜止量測</b>：用與 <code>rewatch_pack</code> 相同的門檻（0.2%／0.05%）算每場 <code>longest_still_seconds</code>，A 版應與 Manim 相近，B 版應把標「長靜止」的各拍壓到 6 s 以下。</li>
<li><b>音訊</b>：A／B 版都用同一條 film 音軌，<code>ffprobe</code> 比總長。</li>
</ol>
<h3>D.5 render 與交付物</h3>
<ul>
<li><code>npx remotion render Act3 out/act3_A.mp4</code>（1080p30）；<code>--props='{"improvements":{…}}'</code> 產 <code>out/act3_B.mp4</code>。</li>
<li><code>compare.py</code> 用 ffmpeg 依 timeline 從 film 切出同樣七段、串成 <code>out/act3_manim.mp4</code>，再 <code>hstack</code> 成三欄並排 <code>out/act3_side_by_side.mp4</code>（Manim｜Remotion A｜Remotion B）。</li>
<li><code>REVIEW-act3-remotion-vs-manim.html</code>（standalone，幀以 base64 內嵌）：逐拍三欄對照幀、onset Δ 表、靜止表、已知差異清單。</li>
<li>可選：A 版跑一次 <code>visual-frame-audit</code>（V1–V10）確認沒有退步。</li>
<li>一個 task 一個 commit；媒體與 <code>node_modules</code> 不進 git。</li>
</ul>
"""


# ----------------------------------------------------------------------------------------------
def build(film_dir: Path) -> str:
    film = film_dir / "ch03_trig_derivatives_mimo.mp4"
    manifest = json.loads((film_dir / "audio_mimo" / "manifest.json").read_text(encoding="utf-8"))
    timeline = json.loads((film_dir / "ch03_trig_derivatives_mimo.timeline.json").read_text(encoding="utf-8"))
    tl = {s["scene_id"]: s for s in timeline["scenes"]}
    mf = {s["scene_id"]: s for s in manifest["scenes"]}

    thumbs: dict[tuple[str, float], str] = {}
    for sid, ts in FRAMES.items():
        for t in ts:
            thumbs[(sid, t)] = grab(film, tl[sid]["start"] + t)

    def img(sid, t, cls="th"):
        start = tl[sid]["start"]
        return (f'<figure class="{cls}"><img src="data:image/jpeg;base64,{thumbs[(sid, t)]}" alt="">'
                f'<figcaption>場內 {t:.2f} s · 片中 {start + t:.2f} s</figcaption></figure>')

    out: list[str] = []
    w = out.append

    # ---------------- header ----------------
    w(HEAD)
    w('<header class="top"><p class="kicker">Remotion pilot · 規劃文件 · 待裁決</p>'
      '<h1>§3.1 第三幕「三角函數的導數」：固定樣式與分鏡</h1>'
      '<p class="lede">把 Manim 版第三幕的<b>畫面</b>改用 Remotion 重做。旁白已鎖定、MiMo 音訊已錄好，一個字都不動。'
      '本文件先把樣式定死（Part A），再逐場逐拍列出分鏡（Part B），最後是待你裁決的事（Part C）與動工計畫（Part D）。'
      '確認後才開始寫 Remotion。</p>'
      f'<p class="meta">資料來源：film <code>{esc(str(film))}</code>（1920×1080＠30，1049.2 s，2026-09-14 render，git <code>fbb9c86</code>）；'
      'manifest＝同目錄 <code>audio_mimo/manifest.json</code>（MiMo <code>mimo-v2.5-tts</code>，voice Dean）；'
      'storyboard＝<code>video/storyboards/ch03_trig_derivatives_mimo.yml</code>（第三幕各場自 fbb9c86 以來沒有變動）。'
      '注意：任務說明寫的 <code>ch03_trig_derivatives.mp4</code> 是 2026-07-02 的 480p／15fps、23.6 s 舊檔，不是成片，本文件一律用 <code>_mimo.mp4</code>。</p>'
      '<nav class="toc"><a href="#A">A 固定樣式</a><a href="#arch">繼承架構</a><a href="#B">B 分鏡</a><a href="#C">C 待裁決</a><a href="#D">D 實作計畫</a></nav></header>')

    # ---------------- act timeline ----------------
    w('<section><h2>第三幕時間軸（pilot 的串接順序）</h2>'
      '<p>pilot 的串接順序是 intro → divider_derivatives → 四個 content 場 → outro。film 裡 intro 後面接的是 divider_limit，這裡跳接，但每場各自的片段與 film 完全相同。'
      '每個 content 場＝lead 1.0 s＋旁白＋tail 1.0 s（timing.py:7-8）；場與場之間各側有 0.2 s 淡黑，淡在片段內部，不增加總長（make.py:986）。</p>'
      '<table class="grid"><tr><th>場</th><th>模板／hook</th><th>film 起訖（s）</th><th>長度</th><th>幀數＠30</th><th>旁白</th></tr>')
    templ = {"intro": "intro", "divider_derivatives": "divider", "derivative_of_sine": "theorem_proof",
             "derivative_of_cosine": "theorem_proof＋cosine_identity_draft", "slope_equals_height": "graph＋slope_equals_height",
             "derivative_cycle": "definition_math＋derivative_cycle", "outro": "outro"}
    total = 0
    for sid in ACT_SCENES:
        s = tl[sid]
        dur = s["end"] - s["start"]
        fr = round(dur * FPS)
        total += fr
        m = mf[sid]
        narr = f'{m.get("audio_seconds", 0):.3f} s，{m.get("beat_count", 0)} 拍' if m.get("beats") else "無（silent）"
        w(f'<tr><td><a href="#s-{sid}"><code>{sid}</code></a></td><td>{templ[sid]}</td><td>{s["start"]:.3f}–{s["end"]:.3f}</td>'
          f'<td>{dur:.3f} s</td><td>{fr}</td><td>{narr}</td></tr>')
    w(f'<tr class="sum"><td colspan="4">合計</td><td>{total}</td><td>{total / FPS:.2f} s</td></tr></table></section>')

    # ---------------- Part A ----------------
    w('<section id="A"><h2>Part A　固定樣式清單（四類全部定死，每場繼承）</h2>'
      '<p class="rule-box"><b>鎖死與可調的原則。</b>hex、字族、字級表、邊距與格線、卡片幾何、各種標準動作的時長與緩動、轉場，全部是 <b>token，鎖死</b>。'
      '場景只能做三件事：(1) 從枚舉裡<b>挑</b>：<code>accent</code>（theorem／remark／…）、<code>reveal kind</code>（fade／slide／write／create／transform）、函數色（<code>deck.sin</code> 等）；'
      '(2) 給<b>內容</b>：標題、motive、式子、軸範圍；(3) hook 元件自己的幾何（例如切線放在哪個 x）。'
      '場景不能寫 hex、px 或秒數。這對應 storyboard 目前的做法：它也只寫 <code>accent</code>／<code>color_role</code>／<code>anim</code> 名字。</p>')

    # A.1
    w('<h3>A.1　配色與語意色</h3><table class="grid colors"><tr><th>token</th><th>色</th><th>第三幕用在哪</th><th>Manim 出處</th><th>Remotion token</th><th>鎖死／可調</th></tr>')
    group = None
    for g, tok, hx, use, src, rt, lock in COLOR_ROWS:
        if g != group:
            w(f'<tr class="grp"><td colspan="6">{g}</td></tr>')
            group = g
        w(f'<tr><td><code>{tok}</code></td><td class="nowrap">{sw(hx)}</td><td>{use}</td><td><code>{src}</code></td><td><code>{rt}</code></td><td>{lock}</td></tr>')
    w('</table>')
    w('<p class="warn"><b>有一件事要先知道：</b>第三幕畫面上的 sin 琥珀、cos 青藍、結論綠，用的是 theme.py 的<b>凍結別名</b>（<code>accent</code>／<code>secondary</code>／<code>success</code>），'
      '不是 Direction B 的色相 token（<code>amber #d98f3c</code>／<code>blue #4fa6de</code>／<code>green #3ebe7c</code>）。theme.py:32-40 標明是否改指仍未決（D2-07）。Remotion 端用 deck 層 token（<code>deck.sin</code> 等）包一層，'
      '日後只要改 token 指向，不用改任何場（Part C-2）。</p>')
    w(f'<p class="note">{GLOW_NOTE}</p>')
    w('<p class="note"><b>語意色的規則（沿 SPEC 規則 5）：</b>sin＝琥珀、cos＝青藍、斜率／結論＝綠，在曲線、讀數、環節點左條上一律同色；函數名 token（\\(\\sin\\)／\\(\\cos\\)）在式子裡<b>不上色</b>'
      '（storyboard:41-43 刻意不進 color_map）；段色／曲線色優先於 token 色。indicate 的閃色：有 accent 的場用 <code>&lt;role&gt;_ink</code>，沒有 accent 的場用 <code>amber_ink</code>（scene.py:211-215）。</p>')

    # A.2
    w('<h3>A.2　字型與公式樣式</h3>'
      '<table class="grid"><tr><th>角色</th><th>現行 Manim（出處）</th><th>Remotion 對應</th><th>鎖死／可調</th></tr>'
      '<tr><td>內文、標題</td><td>Instrument Sans Regular／SemiBold／Bold（repo vendored OTF，<code>video/pipeline/fonts/instrument-sans/otf/</code>），經 LaTeX <code>\\sfdefault</code> 排版、microtype 字距（_bootstrap.py:77-83）；Bold 的字間距修正為 0.2101 em（_bootstrap.py:91-102）</td>'
      '<td><code>@remotion/fonts</code> 的 <code>loadFont()</code> 載入同一批 OTF（放 <code>public/fonts/</code>，版本完全相同）；Bold 字距以 <code>word-spacing</code> 補（量測後定值）</td><td>鎖死</td></tr>'
      '<tr><td>eyebrow、標籤（mono）</td><td>IBM Plex Mono，<code>\\texttt</code>＋全大寫，例如「[ THEOREM ]」「STAGE 3」「PROOF」（brand.py:157-164；由 MiKTeX 的 plex-mono 提供，repo 沒有 vendored）</td>'
      '<td><code>@remotion/google-fonts/IBMPlexMono</code>，或把 woff2 vendored 進 <code>public/fonts/</code>（建議後者，換機不連網也能跑）；<code>text-transform: uppercase</code></td><td>鎖死</td></tr>'
      '<tr><td>數學</td><td>Latin Modern（<code>lmodern</code>，pdflatex→dvisvgm 輸出向量），<code>\\everymath{\\displaystyle}</code>（_bootstrap.py:78,83）</td>'
      '<td>MathJax 4＋<code>mathjax-newcm</code>（New Computer Modern，SVG 輸出，display 模式），建置前預先轉好（Part D）</td><td>鎖死</td></tr>'
      '</table>')
    w('<p><b>字級表</b>：token 單位是「px＠1920×1080」，但它校準的是<b>大寫高</b>，不是 CSS font-size。實測 cap ≈ 0.894 × token（theme.py:65-72；film 上 h1 78 的「T」高 68–69 px）。'
      'Instrument Sans capHeight＝0.72 em，換成 CSS 就是 <b>font-size ≈ 1.242 × token</b>。</p>'
      '<table class="grid"><tr><th>token</th><th>px（theme.py:83-98）</th><th>≈ 大寫高 px</th><th>≈ CSS font-size（Instrument Sans）</th><th>第三幕用途</th></tr>')
    for tok, px, use in TYPE_SCALE:
        w(f'<tr><td><code>{tok}</code></td><td>{px}</td><td>{px * 0.894:.0f}</td><td>{px * 1.242:.1f}</td><td>{use}</td></tr>')
    w('</table><p>數學字級：MathTex 用 <code>font_size = px×0.698</code>（PX_TO_FS，theme.py:60），不乘 TEXT_SCALE。film 實測 step 42 的「cos」x-height ≈ 19 px，推得 em ≈ 44 px，所以 <b>MathJax em ≈ 1.05 × token</b>（Part D 精校）。會用到的數學字級：'
      + "、".join(f"<code>{t}</code> {p}" for t, p in MATH_TIERS) + '。</p>')
    w('<div class="diff"><b>Remotion 會和 Manim 看起來不一樣的地方（先講清楚）：</b><ul>'
      '<li><b>數學字形</b>：New Computer Modern 與 Latin Modern 同出 Knuth 的 Computer Modern，字形幾乎相同，但 MathJax 的排版不是 TeX 本身：\\(\\left(\\;\\right)\\) 的定界符大小、分數線粗細、運算子間距都可能差一兩 px。以 <code>\\cos\\!\\left(x+\\frac h2\\right)</code> 這種列最明顯。</li>'
      '<li><b>文字斷行</b>：Manim 用字元寬估算斷行（brand.py:87-117），瀏覽器用真實字寬，所以 derivative_cycle 的 statement 這類兩行 prose 可能換到別處。A 版要把斷行寫死。</li>'
      '<li><b>字距</b>：LaTeX 有 microtype 的 protrusion，瀏覽器沒有；Bold 的字間距要手動補。</li>'
      '<li><b>光柵化</b>：Cairo 與 Chrome 的反鋸齒不同，細線（hairline、虛線）邊緣會有些微差異，逐幀差分要設門檻。</li>'
      '<li><b>變形的中間幀</b>：Manim 的 TransformMatchingShapes 會讓字形糊成一團（sine 場 15.8 s 那張）。Remotion 走分段平移，中間幀會乾淨很多，但就不可能像素相同；只有起點與終點幀相同。</li>'
      '<li><b>Write</b>：manim 是先描外框再填色，Remotion 預設是逐 token 淡入或 clip 擦出（Part C-7）。</li>'
      '</ul></div>')

    # A.3
    w('<h3>A.3　卡片與版面框架（px＠1080p；1 manim unit＝135 px）</h3>'
      '<table class="grid"><tr><th>項目</th><th>現行 Manim 值（出處）</th><th>Remotion 對應</th><th>鎖死／可調</th></tr>'
      '<tr><td>畫布</td><td>1920×1080＝14.222×8 u（theme.py:231-234）；深色場底色平塗，不畫格線（SHOW_GRID=False，theme.py:280）</td><td><code>&lt;SceneShell ground="dark|paper"&gt;</code></td><td>鎖死</td></tr>'
      '<tr><td>安全區</td><td>上下 74 px（SAFE_MARGIN，theme.py:237）；左右 100 px（SIDE_GUTTER，theme.py:238）</td><td><code>layout.safeY=74</code>、<code>layout.gutter=100</code></td><td>鎖死</td></tr>'
      '<tr><td>格線</td><td>內容寬 1720 px 分 12 欄（每欄 143.3 px，_common.py:40-47）；rail 從第 7 欄開始：RAIL_X≈1103 px，主欄 1003 px，rail 717 px（_common.py:54-57）</td><td><code>layout.col(n)</code>、<code>layout.railX</code></td><td>鎖死</td></tr>'
      '<tr><td>標題列（masthead）</td><td>eyebrow 頂在 y=74 px（MASTHEAD_TOP，_common.py:72），標題在其下 22 px（EYEBROW_GAP，theme.py:243），motive 再往下 0.22u≈30 px；內容區從標題底往下 56 px（TITLE_GAP，theme.py:244）。graph 模板沒有 eyebrow，標題是 0.88×h1（graph.py:152-160）</td><td><code>&lt;Masthead eyebrow title motive/&gt;</code></td><td>鎖死；文字可調</td></tr>'
      '<tr><td>品牌框：spine</td><td>左側 x≈70 px 一條全高 hairline_strong 細線，masthead 那一段是 2.4 寬的 accent 色 cap（_common.py:313-344）；片測 x=69–71 px</td><td>SceneShell 內建</td><td>鎖死（cap 色隨 accent）</td></tr>'
      '<tr><td>品牌框：summit bars</td><td>右下 7 根遞增圓角條，高 0.45u≈61 px，muted，不透明度 0.4（_common.py:441-445；brand.py:828-850）</td><td>SceneShell 內建 <code>&lt;Motif/&gt;</code></td><td>鎖死</td></tr>'
      '<tr><td>theorem statement 卡（rail 卡）</td><td>accent_panel：圓角 12 px（RADIUS_MD）、左條 5 px（BAR_W）、底 panel、hairline 描邊；內距上下 0.34u≈46 px、左右 0.5u≈68 px；右緣貼齊 1820 px，頂端貼內容區頂（theorem_proof.py:167-172,248-250；brand.py:750-779）。太寬的 statement 會升格成全寬 band 卡（theorem_proof.py:88-116）</td><td><code>&lt;Card variant="rail|band" bar={role}&gt;</code></td><td>鎖死；bar 色隨 accent</td></tr>'
      '<tr><td>證明鏈</td><td>左緣＝spine＋0.4u（154 px）；最小列距 0.5u≈68 px，會撐開填滿內容區（theorem_proof.py:54,222）；「PROOF」小標（muted）；qed 列＝success 綠字＋0.46u 方框 ■（theorem_proof.py:152-163）</td><td><code>&lt;ProofChain&gt;</code>（TheoremProof 內部）</td><td>鎖死</td></tr>'
      '<tr><td>definition／remark 版</td><td>單欄靠左：statement（prose 44，ink_1）＋數學列，列距 0.36u，statement 到數學 0.71u，整塊在內容區置中（definition_math.py）</td><td><code>&lt;DefinitionMath&gt;</code></td><td>鎖死</td></tr>'
      '<tr><td>callout／aside 卡</td><td>本幕未用（build_aside＋accent_panel，_common.py:422-439）；一併移植成 <code>&lt;Card variant="aside"&gt;</code>，第三幕以外的場景需要</td><td><code>&lt;Card variant="aside"&gt;</code></td><td>鎖死</td></tr>'
      '<tr><td>環節點卡（hook）</td><td>accent_panel，內距 0.16u／0.26u，math_rail 字級，左條依函數著色（hooks:1237-1241）</td><td><code>&lt;Card variant="node" bar={deck.sin|deck.cos}&gt;</code></td><td>鎖死</td></tr>'
      '<tr><td>座標圖</td><td>軸 muted、stroke 2、箭頭 0.16u；曲線 stroke 5 加 12 寬光暈；axes 依 storyboard 長度建好後，縮放置入標題與底邊之間（graph.py:829-841,843-880）</td><td><code>&lt;Axes&gt;</code>、<code>&lt;FunctionPlot&gt;</code>，座標換算 <code>c2p()</code> 自寫</td><td>鎖死；範圍與長度可調</td></tr>'
      '<tr><td>divider</td><td>左側一疊垂直置中（eyebrow→標題（寬上限 72%）→問題→副標→進度點），間距 0.34／0.42／0.42／0.6u；右側 ghost 數字；hero curve（divider.py:31-100）</td><td><code>&lt;Divider&gt;</code></td><td>鎖死；文字可調</td></tr>'
      '</table>')

    # A.4
    w('<h3>A.4　片頭片尾與轉場、標準動作</h3>'
      '<table class="grid"><tr><th>動作</th><th>現行 Manim（出處）</th><th>Remotion（＠30fps）</th><th>鎖死／可調</th></tr>'
      '<tr><td>場的 lead／tail</td><td>各 1.0 s 靜止（timing.py:7-8）</td><td><code>motion.lead = 30f</code>、<code>motion.tail = 30f</code></td><td>鎖死（同步基準）</td></tr>'
      '<tr><td>場間轉場</td><td>每個邊界各側 0.2 s 淡黑（ffmpeg <code>fade</code>，淡在片段內，不改總長；make.py:665-713,986）</td><td>SceneShell 的邊緣淡黑 overlay，各 6f</td><td>鎖死（C 串經過的邊界例外，見 Part C-6）</td></tr>'
      '<tr><td>fade（預設 reveal）</td><td>0.5 s FadeIn＋上移 0.1u（13.5 px）（blocks.py:138-141；timing.py:21）</td><td><code>&lt;Reveal kind="fade"&gt;</code> 15f</td><td>鎖死</td></tr>'
      '<tr><td>slide（statement）</td><td>0.5 s FadeIn＋右移 0.35u（47 px）（blocks.py:151-154）</td><td><code>kind="slide"</code> 15f</td><td>鎖死</td></tr>'
      '<tr><td>create（曲線）</td><td>0.8 s Create；hook 的切線與 connector 用 0.65 s（hooks:103-107）</td><td><code>kind="create"</code>（<code>evolvePath</code>）24f／20f</td><td>鎖死</td></tr>'
      '<tr><td>write／write_glow／highlight</td><td>0.7／0.8／0.7 s Write（timing.py:24-33）</td><td><code>kind="write"</code> 21f／24f</td><td>鎖死（樣式見 C-7）</td></tr>'
      '<tr><td>transform（token 變形）</td><td>1.2 s；來源列退到 55% 不透明（derivation.py:245,330-361；timing.py:37）</td><td><code>&lt;TokenMorph&gt;</code> 36f＋<code>&lt;Dim to=0.55&gt;</code></td><td>鎖死</td></tr>'
      '<tr><td>frame（變動前框選）</td><td>0.4 s，hairline_strong 框，外擴 0.08u，框在 morph 時淡出（derivation.py:244,261-270）</td><td><code>&lt;FrameBox&gt;</code> 12f</td><td>鎖死</td></tr>'
      '<tr><td>cancel（兩段式消去）</td><td>1.2 s＝0.4 淡出＋0.8 合攏（timing.py:45；derivation.py:364-390）</td><td><code>&lt;CancelTwoStage&gt;</code> 12f＋24f</td><td>鎖死</td></tr>'
      '<tr><td>dim（focus）</td><td>0.4 s，透明度 ×0.35（focus.py:40-41）</td><td><code>&lt;Dim&gt;</code> 12f</td><td>鎖死</td></tr>'
      '<tr><td>indicate</td><td>0.8 s，放大 1.15＋染色再回復（focus.py:43-44,109-124）</td><td><code>&lt;Indicate&gt;</code> 24f，there-and-back</td><td>鎖死；色隨 accent</td></tr>'
      '<tr><td>carry／exit</td><td>carry 飛行 0.8 s；exit 淡出 0.5 s 落在 tail 內（timing.py:41,50）</td><td><code>&lt;Carry&gt;</code> 24f、<code>exit</code> 15f</td><td>鎖死</td></tr>'
      '<tr><td>paced（隨旁白寫）</td><td>寫滿整拍，保留 0.6 s 收尾（timing.py:57-78）</td><td><code>&lt;PacedWrite&gt;</code>，長度＝拍長−18f</td><td>鎖死</td></tr>'
      '<tr><td>緩動</td><td>manim 預設 <code>smooth</code>；Indicate 用 there_and_back</td><td><code>Easing.bezier(0.45,0,0.55,1)</code>（待擬合）；indicate 另寫</td><td>鎖死</td></tr>'
      '<tr><td>片頭（intro）</td><td>米紙三段：logo → 課程地圖（節點轉紅、節名 Create）→ 1.0 s crossfade 進深色場的節標記（scene.py:323-390；intro.py）</td><td><code>&lt;IntroGate&gt;</code>，段落起點用量測幀號</td><td>鎖死；節名與標語讀 meta</td></tr>'
      '<tr><td>divider</td><td>整幅靜止，只有邊界淡黑（scene.py:315-321，無 dynamic block）</td><td><code>&lt;Divider&gt;</code></td><td>鎖死（D1 為可選改良）</td></tr>'
      '<tr><td>片尾（outro）</td><td>米紙，五件依序淡入 0.5 s＋0.12 s 間隔，最後停 ≥2 s（scene.py:392-423；outro.py）</td><td><code>&lt;Outro&gt;</code></td><td>鎖死；Next 讀 storyboard</td></tr>'
      '<tr><td>拍內順序</td><td>dim → rider（PROOF 小標）→ reveal → indicate；拍長＝旁白長，以累計目標對齊，誤差不累積（scene.py:196-313）</td><td><code>&lt;BeatTimeline&gt;</code> 依 act3.json 的幀號</td><td>鎖死</td></tr>'
      '</table>')

    # architecture
    w('<h3 id="arch">繼承架構</h3>' + ARCH_SVG)
    w('<p>新場景怎麼繼承外觀（示意 TSX，只有幾行）：</p><pre class="code">' + esc(EXAMPLE_TSX) + '</pre>')
    w('</section>')

    # ---------------- Part B ----------------
    w('<section id="B"><h2>Part B　分鏡</h2>'
      '<p>時間欄寫「場內秒」（含 1.0 s lead，也就是場的時鐘），括號內是 film 片中的秒數。旁白一字不改，直接取自 manifest 的 <code>beats[].text</code>（MiMo 口語版）。'
      '<span class="badge still">長靜止</span>＝未宣告靜止超過 6 s（SPEC 規則 4）。<span class="badge imp">改良提案</span>＝Remotion 容易做到的視覺改良，逐條請你決定要不要；'
      '沒標的就是「照 Manim 搬，換成 Remotion 元件」。揭示順序與教學內容都跟 Manim 版相同。</p>')
    w(f'<p class="note">{C_CHAIN}</p>')

    for sid in ACT_SCENES:
        spec = SCENES[sid]
        s = tl[sid]
        dur = s["end"] - s["start"]
        w(f'<article class="scene" id="s-{sid}"><h3><code>{sid}</code>　<span class="dur">{dur:.3f} s · {round(dur * FPS)} 幀 · film {s["start"]:.3f}–{s["end"]:.3f}</span></h3>'
          f'<p class="sm"><b>Manim：</b>{spec["template"]}<br><b>Remotion：</b>{spec["remotion"]}<br><b>音訊：</b>{spec["audio"]}</p>')
        if "stages" in spec:
            w('<div class="beat"><div class="thumbs">' + "".join(img(sid, t) for t in FRAMES[sid]) + '</div><div class="txt">'
              '<table class="grid stages"><tr><th>場內秒</th><th>現行 Manim 畫面</th></tr>'
              + "".join(f'<tr><td class="nowrap">{a}</td><td>{b}</td></tr>' for a, b in spec["stages"])
              + f'</table><p><b>Remotion：</b>{spec["remotion_body"]}</p>')
            for code, text, rule in spec["proposals"]:
                w(f'<p class="imp"><span class="badge imp">改良提案 {code}</span> {text} <span class="rule">{rule}</span></p>')
            w('</div></div>')
        else:
            beats = mf[sid]["beats"]
            for idx in sorted(spec["beats"]):
                b = spec["beats"][idx]
                if idx == 0:
                    t0, t1, text, reveal = 0.0, 1.0, "（lead，無旁白）", "—"
                else:
                    mb = beats[idx - 1]
                    t0, t1 = 1.0 + mb["start_seconds"], 1.0 + mb["end_seconds"]
                    text, reveal = mb["text"], mb["reveal"] or "（無）"
                still = f' <span class="badge still">{b["still"]}</span>' if b.get("still") else ""
                thumbs_html = "".join(img(sid, t) for t in b["frames"]) or '<p class="nofr">（畫面同上一格）</p>'
                w(f'<div class="beat"><div class="bh"><span class="bi">beat {idx}</span> <code>{esc(str(reveal))}</code> '
                  f'<span class="bt">{t0:.2f}–{t1:.2f} s（片中 {s["start"] + t0:.2f}–{s["start"] + t1:.2f}）· {t1 - t0:.2f} s</span>{still}</div>'
                  f'<blockquote>{esc(text)}</blockquote>'
                  f'<div class="thumbs">{thumbs_html}</div><div class="txt">'
                  f'<p><b>現行 Manim：</b>{b["manim"]}</p><p><b>Remotion：</b>{b["remotion"]}</p>'
                  f'<p class="rule">對應規則：{b["rule"]}</p>')
                for code, text2 in b.get("improve", []):
                    w(f'<p class="imp"><span class="badge imp">改良提案 {code}</span> {text2}</p>')
                w('</div></div>')
            last = beats[-1]
            tail0 = 1.0 + last["end_seconds"]
            w(f'<p class="sm">tail：{tail0:.2f}–{dur:.2f} s 靜止（旁白結束後 1.0 s），之後 0.2 s 淡黑出場。</p>')
        w('</article>')
    w('</section>')

    # ---------------- Part C ----------------
    w('<section id="C"><h2>Part C　待裁決</h2><ol class="dec">')
    for title, q, rec in DECISIONS:
        w(f'<li><b>{title}</b>：{q}<br><span class="rec">建議：{rec}</span></li>')
    w('</ol></section>')

    # ---------------- Part D ----------------
    w('<section id="D"><h2>Part D　實作計畫（下一步）</h2>' + PART_D + '</section>')
    w('<section><h2>尚未確定的事</h2><ul>'
      '<li>MathJax em 與 Manim 數學字級的精確換算，目前只有 film 上一次 x-height 的估計（≈1.05×token）。</li>'
      '<li>IBM Plex Mono 的 eyebrow 在 film 上的實際字高（沒有量）；manim stroke 單位換成 px 的倍率（推估 1.35）。</li>'
      '<li>intro 各段的精確起點：code 推算合計 10.44 s，film 實為 10.3 s，要從 film 量。</li>'
      '<li>manim <code>smooth</code> 緩動曲線的 bezier 近似，要擬合。</li>'
      '<li>derivative_of_cosine 在 manifest 裡沒有 forced-alignment 的 words 檔（<code>beats</code> 模式），所以 K2／K3 的逐字時間要先在本機對齊，或沿用比例切點。</li>'
      '<li>Remotion 授權是否適用本計畫（見 C-11）。</li>'
      '</ul><p class="sm">本檔由 <code>video/experiments/remotion_pilot/build_plan.py</code> 產生（ffmpeg 抽幀，480 px JPEG q70，以 base64 內嵌）。</p></section>')
    w('</main></body></html>')
    return "\n".join(out)


HEAD = r"""<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Remotion 第三幕規劃</title>
<script>window.MathJax={tex:{inlineMath:[['\\(','\\)']],displayMath:[['\\[','\\]']]},svg:{fontCache:'global'}};</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
<style>
:root{--bg:#f7f6f2;--fg:#1c2130;--mut:#5d6474;--line:#d9d6cc;--card:#fff;--acc:#0068a7;--imp:#b76e00;--warn:#aa3333;--code:#eef0f4}
@media (prefers-color-scheme: dark){:root{--bg:#0f1520;--fg:#e6eaf2;--mut:#9aa3b5;--line:#2a3448;--card:#151d2c;--acc:#79bfe8;--imp:#e8ab63;--warn:#e88f8f;--code:#1d2638}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.65 system-ui,-apple-system,"Segoe UI","Noto Sans TC","Microsoft JhengHei",sans-serif}
main{max-width:1180px;margin:0 auto;padding:24px 16px 80px}
h1{font-size:28px;line-height:1.3;margin:.2em 0}h2{font-size:22px;margin:2.2em 0 .6em;padding-top:.6em;border-top:2px solid var(--line)}h3{font-size:17px;margin:1.6em 0 .5em}
code{font:12.5px/1.4 ui-monospace,Consolas,monospace;background:var(--code);padding:1px 4px;border-radius:3px}
pre{background:var(--code);padding:12px 14px;border-radius:6px;overflow-x:auto;font:12.5px/1.5 ui-monospace,Consolas,monospace}
pre code{background:none;padding:0}
.kicker{color:var(--acc);font-weight:600;letter-spacing:.04em;margin:0}.lede{font-size:16px}.meta,.sm{color:var(--mut);font-size:13px}
.toc a{display:inline-block;margin:6px 10px 0 0;color:var(--acc)}
table.grid{border-collapse:collapse;width:100%;margin:.6em 0;font-size:13.5px;background:var(--card)}
table.grid th,table.grid td{border:1px solid var(--line);padding:5px 7px;vertical-align:top;text-align:left}
table.grid th{background:var(--code)}tr.grp td{background:var(--code);font-weight:600}tr.sum td{font-weight:600}
.nowrap{white-space:nowrap}.sw{display:inline-block;width:22px;height:16px;border:1px solid #0003;border-radius:3px;vertical-align:middle;margin-right:5px}
.note,.rule-box,.warn,.diff{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--acc);padding:8px 12px;border-radius:4px;margin:.8em 0}
.warn{border-left-color:var(--warn)}.diff{border-left-color:var(--imp)}.diff ul{margin:.3em 0 0 1.1em;padding:0}
article.scene{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px 16px 12px;margin:22px 0}
article.scene h3{margin-top:.3em}.dur{color:var(--mut);font-weight:400;font-size:13px}
.beat{border-top:1px dashed var(--line);padding:10px 0;display:grid;grid-template-columns:minmax(0,1fr);gap:6px}
.bh{font-size:14px}.bi{font-weight:700;color:var(--acc)}.bt{color:var(--mut);font-size:13px;margin-left:6px}
blockquote{margin:2px 0 4px;padding:4px 10px;border-left:3px solid var(--line);color:var(--fg);font-style:italic;font-size:14px}
.thumbs{display:flex;flex-wrap:wrap;gap:8px}figure.th{margin:0;width:min(100%,320px)}figure.th img{width:100%;display:block;border-radius:4px;border:1px solid var(--line)}
figcaption{font-size:11.5px;color:var(--mut)}.nofr{color:var(--mut);font-size:12.5px;margin:0}
.txt p{margin:.3em 0}.rule{color:var(--mut);font-size:12.5px}
.badge{display:inline-block;font-size:11.5px;font-weight:700;padding:1px 7px;border-radius:10px;margin-right:4px;white-space:nowrap}
.badge.still{background:var(--warn);color:#fff}.badge.imp{background:var(--imp);color:#fff}
p.imp{border:1px solid var(--imp);border-radius:5px;padding:5px 9px;background:color-mix(in srgb,var(--imp) 7%,transparent)}
ol.dec li{margin:.7em 0}.rec{color:var(--acc)}
svg.arch{width:100%;height:auto;max-width:1100px;display:block;margin:.6em 0}
svg.arch rect{fill:var(--card);stroke:var(--line)}svg.arch text{fill:var(--fg);font:13px system-ui,sans-serif}
svg.arch .lab{font-weight:700;fill:var(--acc)}svg.arch .ar{stroke:var(--mut);stroke-width:1.5;fill:none;marker-end:url(#ah)}
svg.arch .band{fill:var(--code);stroke:none}
@media (max-width:640px){body{font-size:14px}table.grid{display:block;overflow-x:auto}}
</style></head><body><main>
"""

ARCH_SVG = r"""<svg class="arch" viewBox="0 0 1100 470" role="img" aria-label="繼承層次圖">
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#8a93a6"/></marker></defs>
<rect class="band" x="0" y="0" width="1100" height="80" rx="6"/><text class="lab" x="14" y="24">① theme tokens（鎖死）</text>
<rect x="14" y="34" width="250" height="36" rx="5"/><text x="26" y="57">color：dark／paper／role／deck</text>
<rect x="276" y="34" width="250" height="36" rx="5"/><text x="288" y="57">type：字族＋字級（cap 校準）</text>
<rect x="538" y="34" width="250" height="36" rx="5"/><text x="550" y="57">layout：安全區／12 欄／rail</text>
<rect x="800" y="34" width="286" height="36" rx="5"/><text x="812" y="57">motion：時長＋緩動＋lead／tail</text>
<rect class="band" x="0" y="100" width="1100" height="120" rx="6"/><text class="lab" x="14" y="124">② base components（只讀 tokens）</text>
<rect x="14" y="134" width="150" height="36" rx="5"/><text x="26" y="157">SceneShell</text>
<rect x="174" y="134" width="160" height="36" rx="5"/><text x="186" y="157">Masthead・Card</text>
<rect x="344" y="134" width="180" height="36" rx="5"/><text x="356" y="157">MathTex（MathJax）</text>
<rect x="534" y="134" width="260" height="36" rx="5"/><text x="546" y="157">Reveal・Dim・Indicate・FrameBox</text>
<rect x="804" y="134" width="282" height="36" rx="5"/><text x="816" y="157">TokenMorph・CancelTwoStage</text>
<rect x="14" y="176" width="250" height="36" rx="5"/><text x="26" y="199">BeatTimeline（act3.json → 幀）</text>
<rect x="276" y="176" width="300" height="36" rx="5"/><text x="288" y="199">Axes・FunctionPlot・Tangent</text>
<rect x="588" y="176" width="260" height="36" rx="5"/><text x="600" y="199">PacedWrite・Carry（C 串用）</text>
<rect class="band" x="0" y="240" width="1100" height="80" rx="6"/><text class="lab" x="14" y="264">③ templates（對應 Manim 同名模板）</text>
<rect x="14" y="274" width="160" height="36" rx="5"/><text x="26" y="297">IntroGate</text>
<rect x="184" y="274" width="140" height="36" rx="5"/><text x="196" y="297">Divider</text>
<rect x="334" y="274" width="130" height="36" rx="5"/><text x="346" y="297">Outro</text>
<rect x="474" y="274" width="190" height="36" rx="5"/><text x="486" y="297">TheoremProof</text>
<rect x="674" y="274" width="140" height="36" rx="5"/><text x="686" y="297">Graph</text>
<rect x="824" y="274" width="262" height="36" rx="5"/><text x="836" y="297">DefinitionMath</text>
<rect class="band" x="0" y="340" width="1100" height="120" rx="6"/><text class="lab" x="14" y="364">④ scene data＋hook 元件（場景只給內容與枚舉選擇）</text>
<rect x="14" y="374" width="400" height="36" rx="5"/><text x="26" y="397">act3.json ← storyboard _mimo.yml＋manifest＋timeline</text>
<rect x="424" y="374" width="220" height="36" rx="5"/><text x="436" y="397">CosineIdentityDraft</text>
<rect x="654" y="374" width="210" height="36" rx="5"/><text x="666" y="397">SlopeEqualsHeight</text>
<rect x="874" y="374" width="212" height="36" rx="5"/><text x="886" y="397">DerivativeCycleRing</text>
<text x="26" y="440">zod schema 驗 props；improvements 開關（B 版）；hook 只能用 ② 的元件＋tokens，不寫 hex／px／秒</text>
<path class="ar" d="M550,80 L550,98"/><path class="ar" d="M550,220 L550,238"/><path class="ar" d="M550,320 L550,338"/>
</svg>"""

EXAMPLE_TSX = """// src/scenes/DerivativeOfSine.tsx —— 新場景只給內容，外觀全由模板＋tokens 決定
import {TheoremProof} from '../templates/TheoremProof';
import {useScene} from '../components/BeatTimeline';

export const DerivativeOfSine: React.FC = () => {
  const spec = useScene('derivative_of_sine');        // 來自 act3.json（storyboard＋manifest）
  return <TheoremProof spec={spec} accent="theorem" />; // accent 只能選枚舉 → role.result 藍
};

// templates/TheoremProof.tsx（節錄）：模板把 beat id 接到標準動作
<SceneShell ground="dark" accent={role}>              {/* 安全區、spine、motif、邊緣淡黑 */}
  <Masthead eyebrow="[ theorem ]" title={spec.title} motive={spec.scaffold?.motive} />
  <Beat id="statement"><Reveal kind="slide"><Card variant="rail" bar={role}>
    <MathTex tex={spec.statement} size="statement" /></Card></Reveal></Beat>
  <Beat id="proof.1"><FrameBox target="proof.0" /><TokenMorph from="proof.0" to="proof.1" /></Beat>
  <Beat id="qed"><Reveal kind="fade"><QedRow tex={spec.qed} /></Reveal><Indicate target="statement" /></Beat>
</SceneShell>"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--film-dir", type=Path,
                    default=main_checkout() / "video" / "output" / "ch03" / "s3.1")
    args = ap.parse_args()
    OUT_HTML.write_text(build(args.film_dir), encoding="utf-8")
    print(f"wrote {OUT_HTML} ({OUT_HTML.stat().st_size / 1e6:.2f} MB)")


if __name__ == "__main__":
    main()
