/**
 * Every English string Q7 sets on screen, grouped by scene. zh.ts has the same
 * shape (the `Strings` type enforces it); the scenes read the table for the
 * current `lang` through `useT()` (../kit.tsx). Geometry and motion live only
 * in the scenes — one animation, two languages.
 *
 * Inline markup in prose strings (rendered by `rich`, ../kit.tsx):
 *   {home:…} {pocket:…} {edge:…} {ochre:…}   a span in that semantic colour
 *   {i:…} {i.edge:…}                           emphasis: italic in English;
 *                                              in Chinese weight 600 (+ colour), never italic
 *   $…$                                        inline TeX (Pagella), e.g. $(p,q)$
 *   \n                                         line break
 * Keys ending in `Tex` are whole TeX sources (no markup, and never Chinese
 * inside \text{} — MathJax cannot measure it; split into text + TeX instead).
 * `{n}` is a number slot filled by `fmt`.
 */
import { CARD } from "./card";

export const en = {
  /** running head, left half */
  head: "NTU Science Talent Program · 2026 Exam",
  logo: { sub: CARD.logoSub },
  exam: {
    card: CARD,
    title: "Problem 7",
    kicker: "Problem 7 · Square billiards",
    /** the page is a translation: say so, set as a footnote ("" = none) */
    footnote: "Translated from the Chinese original.",
    setup:
      "A square billiard table has a pocket at each of its four corners. A ball, treated as a point, is placed at the exact center of the table and struck. It travels in a straight line and bounces off the edges by the law of reflection; once it falls into a pocket, the motion ends.",
    theta: "Let {i.ochre:θ} be the angle between the shot direction and the bottom edge.",
    labelA: "(a)",
    parta:
      "Our goal: after the shot, the ball returns to the center of the table before falling into any pocket. Prove that infinitely many angles {i:θ} ∈ [0, 2{i:π}) achieve this.",
    labelB: "(b)",
    partb: "Now the table also has a pocket at the midpoint of each edge. How many angles satisfy the requirement in (a)? Explain.",
    figPath: "the ball’s path",
    figEnd: "into a pocket: the end",
    /** legend entries beside a dot and a ring ("" = no legend row) */
    legendStart: "start (center)",
    legendPocket: "pocket",
    /** one caption line under both figures instead of the legend ("" = none) */
    figNote: "",
    fig3: "the table in (b): eight pockets",
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
    title: "A dictionary",
    real: "the real table",
    kicker: "Coordinates",
    tableIs: "The real table is",
    wide: "so every copy is 2 units wide.",
    evenEven: "(even, even)",
    homeNote: "a copy of the center: the ball is home",
    oddOdd: "(odd, odd)",
    cornerNote: "a copy of a corner: the ball falls in",
    question: "Does the ray from the origin hit another {home:blue} point before a {pocket:red} one?",
  },
  halfway: {
    title: "The halfway test",
    kicker: "The halfway test",
    aim: "To come home, aim at a blue point",
    firstBlue: "first blue point on the ray:",
    firstLattice: "first lattice point on the ray: {edge:(p, q)}\nthe next: (2p, 2q)",
    onlyList: "Only lattice points on the segment:",
    hangs: "Everything hangs on the midpoint {edge:(p, q)}.",
    arrow: "→",
    /** [condition, outcome] — outcome colours (pocket / home / ink3) are set by the scene */
    cases: [
      ["{i:p}, {i:q} both odd", "a corner: pocketed halfway"],
      ["one odd, one even", "safe: the ball comes home"],
      ["both even", "impossible, as gcd = 1"],
    ] as Array<[string, string]>,
  },
  foldback: {
    title: "Fold it back",
    kicker: "Fold it back",
    aimA: "aim at (2, 0); the midpoint (1, 0) is safe",
    aimB: "aim at (4, 2); the midpoint (2, 1) is safe",
    bounces: "Bounces",
    forHome: "For a shot that makes it home:",
    crosses: "It crosses {edge:|p| vertical} and {edge:|q| horizontal} walls:",
    /** followed by the coloured 3 */
    countTex: "\\text{bounces} = |p|+|q| = 2+1 = ",
    /** zh only: the count as prose + inline TeX, in place of countTex ("" = use countTex) */
    countLine: "",
  },
  angles: {
    title: "Back to the angle",
    kicker: "Back to the angle",
    dirTex: "\\text{direction}\\ \\ (p,\\,q)",
    /** zh only: prose + inline TeX in place of dirTex ("" = use dirTex) */
    dirLine: "",
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
    /** right-hand side of  gcd(p,q)=1 ⇒ (p,q) ≠ … */
    evenTex: "(\\text{even},\\text{even})",
    /** zh only: the whole test line as prose + inline TeX, in place of the formula ending in evenTex ("" = formula) */
    testLine: "",
    cut: "The midpoint is always a pocket: every trip home is cut halfway.",
    answer: "angles in (b):",
  },
  recap: {
    title: "Recap",
    a: "(a) Four corner pockets",
    b: "(b) Eight pockets",
    many: "infinitely many angles",
    none: "no angle at all",
    /** the big ∞ set in TeX instead of text ("" = the text ∞) */
    infTex: "",
    idea1: "{i:Unfolding} turns bounces into a straight line.",
    idea2: "{i:The halfway test} turns the line into a question of even and odd.",
  },
  writeup: {
    title: "Writing it up",
    kicker: "How to write it on the exam",
    solution: "Solution.",
    /** [head, body] */
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
    ] as Array<[string, string]>,
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

export type Strings = typeof en;
