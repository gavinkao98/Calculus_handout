/**
 * 中文版 Q7 的畫面字串，與 en.ts 同形狀（`Strings` 型別強制 key 一致）。
 * 標記語法見 en.ts 檔頭；中文專屬規則（STYLE.md「中文版排版」）：
 *   - 數學一律寫成 $…$（TeX），不要用 {i:p} 之類的斜體拉丁字母代替；
 *     $…$ 前後不要自己加空格（與漢字相鄰時自動留 0.18 em）。
 *   - {i:…} 在中文是「強調」＝600 字重（＋語意色），絕不是斜體。
 *   - 全形標點（，。：；？（）「」）；阿拉伯數字與漢字之間照台灣慣例留半形空格（「115 學年度」）。
 *   - 需要控制斷行處用 \n。
 *   - `…Tex` 欄位是整條 TeX：\text{} 裡不能放中文（MathJax 量不到寬度，渲染時會擋下）。
 * 改完字串要重跑 `node scripts/cjk-subsets.mjs`（重新挑 Noto Serif TC 分片）。
 *
 * 用字照 q7/GLOSSARY.zh.md 與 2026-09-26 裁決：回到中心（不說回家）、鏡像桌（不說複本）、
 * 偶數偶數點／奇數奇數點、洞／掉進洞裡（考卷原文）、原本的桌子、中點測試。
 * 狀態（2026-09-26）：head、exam、dictionary、halfway 為暫定中文（驗證機制用；
 * exam 下半頁為考卷原文）；其餘場仍是英文副本，待中文旁白與術語表定稿後替換。
 */
import { CARD } from "./card";
import type { Strings } from "./en";

export const zh: Strings = {
  head: "臺大北區科學人才培育計畫・115 學年度入學考",
  logo: { sub: CARD.logoSub },
  exam: {
    card: CARD,
    title: "第 7 題",
    kicker: "第 7 題・正方形撞球桌",
    footnote: "",
    // 115 學年度入學考第 7 題，考卷原文（逐字）
    setup:
      "考慮一張正方形的撞球桌，四個角落各有一個洞。我們在桌面正中央放一顆球，並將它視為一個質點。球被擊出後會沿直線前進，碰到桌邊時依反射定律反彈；一旦掉進洞裡，運動就結束。",
    theta: "以{ochre:$\\theta$}表示擊球方向與桌子底邊的夾角（見下圖）。",
    labelA: "(a)",
    parta: "我們的目標是：把球擊出之後，讓它在掉進洞之前能夠回到桌子的中心。請證明滿足此要求的擊球角度$\\theta\\in[0,2\\pi)$有無窮多個。",
    labelB: "(b)",
    partb: "考慮下圖的球桌：桌面一樣是正方形，除了四個角落各有一個洞之外，四個邊的中點也各多了一個洞。請問此時滿足 (a) 中要求的擊球角度共有幾個？請說明理由。",
    figPath: "球的路徑",
    figEnd: "掉進洞裡，結束",
    legendStart: "",
    legendPocket: "",
    figNote: "（圖中實心圓為球的起始位置，即桌子中心；\n空心圓為洞）",
    fig3: "(b) 的球桌：八個洞",
  },
  hook: {
    title: "A few shots",
    shot: "Shot {n}",
    captions: ["straight into a {pocket:corner}", "one bounce, then a {pocket:corner}", "still going …", "{home:home}, after three bounces"],
    question: "Which shots come {home:home}?",
    hopeless: "Chasing bounces one by one is hopeless — we need a better picture.",
  },
  mirror: {
    title: "A bounce is a mirror",
    beyond: "beyond the wall",
    kicker: "The law of reflection",
    law: "Angle in {ochre:=} angle out.",
    image: "So the bounced path is the {i.edge:mirror image} of the path with no wall.",
    note: "Turn it over the wall, and it lands exactly on the straight line.",
  },
  unfold: {
    title: "Unfold the table",
    home: "home",
    real: "the real table",
    kicker: "Unfolding",
    easy: "Bounces are hard. Straight lines are easy.",
    across: "At each bounce, mirror the table across",
    steps: ["the right wall", "the top wall", "the next wall"],
    line: "One straight line, ending at the center of a copy: the ball is {home:home}.",
    plane: "Mirrored in every direction, the copies tile the plane. Every shot is a straight line.",
  },
  dictionary: {
    title: "座標字典",
    real: "原本的桌子",
    kicker: "座標",
    tableIs: "原本的桌子是",
    wide: "所以每張鏡像桌寬 2 個單位。",
    evenEven: "偶數偶數點",
    homeNote: "鏡像桌的中心：球回到中心",
    oddOdd: "奇數奇數點",
    cornerNote: "鏡像桌的角落：球掉進洞裡",
    question: "從原點出發的射線，會先碰到\n另一個{home:偶數偶數點}，\n還是先碰到{pocket:奇數奇數點}？",
  },
  halfway: {
    title: "中點測試",
    kicker: "中點測試",
    aim: "要回到中心，就瞄準偶數偶數點",
    firstBlue: "第一個偶數偶數點：",
    firstLattice: "射線上的第一個格點：{edge:$(p,q)$}\n下一個：$(2p,2q)$",
    onlyList: "線段上的格點只有：",
    hangs: "一切都取決於中點{edge:$(p,q)$}。",
    arrow: "→",
    cases: [
      ["$p$、$q$都是奇數", "角落的洞：{i:半路掉進洞裡}"],
      ["一奇一偶", "中點沒有洞：回到中心"],
      ["都是偶數", "不可能：$p$、$q$互質"],
    ],
  },
  foldback: {
    title: "Fold it back",
    kicker: "Fold it back",
    aimA: "aim at (2, 0); the midpoint (1, 0) is safe",
    aimB: "aim at (4, 2); the midpoint (2, 1) is safe",
    bounces: "Bounces",
    forHome: "For a shot that makes it home:",
    crosses: "It crosses {edge:|p| vertical} and {edge:|q| horizontal} walls:",
    countTex: "\\text{bounces} = |p|+|q| = 2+1 = ",
  },
  angles: {
    title: "Back to the angle",
    kicker: "Back to the angle",
    dirTex: "\\text{direction}\\ \\ (p,\\,q)",
    coprime: "no common factor; one odd, one even",
    proved: "Infinitely many angles. (a) is proved.",
    irrational: "An irrational slope never meets another lattice point: never pocketed, never home.",
    vertical: "(0, 1) works too",
  },
  twist: {
    title: "Part (b)",
    kicker: "Part (b)",
    add: "Add a pocket at the middle of every edge.",
    copies: "Their copies: {edge:(odd, even)} and {edge:(even, odd)}.",
    every: "Now every lattice point is a pocket, except {home:(even, even)}.",
    evenTex: "(\\text{even},\\text{even})",
    cut: "The midpoint is always a pocket: every trip home is cut halfway.",
    answer: "angles in (b):",
  },
  recap: {
    title: "Recap",
    a: "(a) Four corner pockets",
    b: "(b) Eight pockets",
    many: "infinitely many angles",
    none: "no angle at all",
    idea1: "{i:Unfolding} turns bounces into a straight line.",
    idea2: "{i:The halfway test} turns the line into a question of even and odd.",
  },
  writeup: {
    title: "Writing it up",
    kicker: "How to write it on the exam",
    solution: "Solution.",
    steps: [
      [
        "Unfold.",
        "Reflect the table across its walls. The path becomes a straight ray from the origin, in direction $(\\cos\\theta,\\,\\sin\\theta)$, across a plane tiled by copies of $[-1,1]^2$.",
      ],
      [
        "Name the points.",
        "Copies of the center: {home:$(2m,\\,2n)$}. Corner pockets: {pocket:(odd, odd)}. In (b), the edge pockets add {edge:(odd, even)} and {edge:(even, odd)}.",
      ],
      [
        "Check the midpoint.",
        "Coming home means reaching some $(2p,\\,2q)$, $\\gcd(p,q)=1$, first. The only lattice point strictly between is {edge:$(p,\\,q)$}.",
      ],
      [
        "Conclude.",
        "(a) If $p+q$ is odd, $(p,q)$ is no pocket; $\\tan\\theta=2k$ for every integer $k$ gives infinitely many $\\theta$. (b) $(p,q)$ is never (even, even), so it is always a pocket: {pocket:no angle works}.  ∎",
      ],
    ],
  },
  epilogue: {
    title: "Beyond this problem",
    kicker: "Beyond this problem",
    shoot: "Shoot at slope",
    irrational: "Irrational: the line never meets another lattice point, so the ball never stops.",
    dense: "Left to run, the path comes arbitrarily close to every point of the table.",
    count: "bounces so far: {n}",
    torus: "(Unfolded, it is one straight line on a torus. Shown here, not proved.)",
  },
  outro: {
    end: "End of Problem 7",
    title: "Square Billiards",
    answer: "(a) {home:infinitely many}  ·  (b) {pocket:none}",
  },
};
