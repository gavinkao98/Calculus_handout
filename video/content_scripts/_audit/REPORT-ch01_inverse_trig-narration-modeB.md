# §1.2 Inverse Trigonometric Functions — Mode B narration audit (curated)

> **Deck:** `ch01_inverse_trig`. **Reviewer:** codex (read-only), prompt
> [`PROMPT-ch01_inverse_trig-narration-modeB.md`](PROMPT-ch01_inverse_trig-narration-modeB.md),
> raw transcript [`REPORT-ch01_inverse_trig-narration-modeB.raw.txt`](REPORT-ch01_inverse_trig-narration-modeB.raw.txt).
> **CONTENT_APPROVED = no** → dimension **D7 (math-content correctness) ran** (required when narration is not yet user-approved).
> **Audited:** source narration ([`ch01_inverse_trig.md`](../ch01_inverse_trig.md)), Version A HTML
> ([`ch01_inverse_trig_narration.html`](../ch01_inverse_trig_narration.html)), Version B spoken
> ([`ch01_inverse_trig_narration_spoken.md`](../ch01_inverse_trig_narration_spoken.md)).

## Verdict: 2 blocking, 1 advisory — **all 3 adopted**

| # | Dim | Unit | Finding | Disposition |
|---|---|---|---|---|
| 1 | D3 | u8 `arcsin_evaluate` | $\tfrac{1}{2\sqrt2}$ read as “one over two times the square root of two” → mishearable as $(1/2)\sqrt2$ | **Adopted** → “one divided by **the quantity** two times the square root of two” |
| 2 | D3 | u13 `signs_from_range` | $\tfrac{\sqrt3}{2}$ → “the square root of three over two”, and $-\tfrac{2\sqrt5}{5}$ → “…over five”: radical/fraction scope ambiguous | **Adopted** → “the square root of three, **divided by** two” / “negative **the quantity** two times the square root of five, **all over** five” |
| 3 | D2 (adv) | generated header | Version-B md header claimed narration “已認可” while approval is pending | **Adopted** → generator header generalised to “忠於內容稿 `narration`” (drops the approved claim; still true for already-approved decks) |

All three fixes are in the **spoken track only** (`.spoken.yml` / generator). The on-screen math in the
canonical storyboard renders as proper stacked fractions and was never ambiguous; only the read-aloud
grouping was. `{show}` markers unchanged → `derive_spoken --check` parity preserved.

## Clean dimensions
- **D7 (math-content) — CLEAN.** codex independently recomputed every value/sign/interval/quadrant:
  `arcsin(1/2)=π/6`, `tan(arcsin 1/3)=1/(2√2)`, `arcsin(sin π)=0`, `sin(arccos(-1/2))=√3/2`,
  `sec(arctan 10)=√101`, `tan(arcsin(-2√5/5))=-2`, `cos(arctan x)=1/√(1+x²)`, and the `arccsc`
  convention example (`f(±1)=π`; alt convention `f(-1)=-π`) — all correct.
- **D1 (Version A faithfulness) — CLEAN.** ids/order/kinds and narration text match source; no MathJax issue.
- **D2 (Version B prose) — CLEAN** apart from the header note above; English wording faithful, only math naturalised.
- **D4 (register) — CLEAN** apart from the D3 grouping fixes.
- **D6 (TTS setup) — CLEAN.** `mimo-v2.5-tts`, voice `Mia`, WAV 24k/mono/PCM16, message shape consistent with `pipeline/tts.py`.

## D5 convention adopted (durable)
codex recommended: complex fractional **products/radicals** in numerator or denominator should be read with
“**the quantity …**” or “**… all over …**”. Added as a row to the universal reading-conventions table in
[`pipeline/derive_spoken.py`](../../pipeline/derive_spoken.py) (`MD_CONFIG_AND_CONVENTIONS`), so every
section's generated `_narration_spoken.md` carries it.

## Regression (post-fix)
Per CLAUDE.md regression rule (manual comparison permitted): the three rewrites are codex's own verbatim
suggestions, disambiguate grouping without altering the mathematics (values above unchanged), introduce no
`$`, and leave `{show}` markers intact. `derive_spoken --check` re-run → **parity OK**; `_mimo.yml` +
`_narration_spoken.md` regenerated. No new issues introduced.
