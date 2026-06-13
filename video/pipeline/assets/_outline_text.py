#!/usr/bin/env python3
"""Convert lockup-color.svg <text> elements to <path> outlines.

Uses fonttools to extract glyph vector outlines from Noto Sans TC (variable
font), so Manim's SVGMobject can load the full lockup without dropping the
Chinese wordmark (SVGMobject only renders <path>/<rect>/<line>, not <text>).

Run once; output is lockup-color-outlined.svg in the same directory.
"""
from __future__ import annotations

from pathlib import Path

from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

FONT_NOTO = Path("C:/Windows/Fonts/NotoSansTC-VF.ttf")
FONT_INTER = Path.home() / "AppData/Local/Microsoft/Windows/Fonts/Inter-VF.ttf"
HERE = Path(__file__).resolve().parent
OUT = HERE / "lockup-color-outlined.svg"


class _Renderer:
    def __init__(self, weight: int, font_path: Path = FONT_NOTO):
        self._font = TTFont(str(font_path))
        loc = {"wght": weight}
        if "opsz" in {a.axisTag for a in self._font["fvar"].axes}:
            loc["opsz"] = 14
        self._gs = self._font.getGlyphSet(location=loc)
        self._cmap = self._font.getBestCmap()
        self._upem = self._font["head"].unitsPerEm

    def close(self):
        self._font.close()

    def _glyph_path(self, char: str, size: float, x: float, y: float):
        name = self._cmap.get(ord(char))
        if not name:
            return "", 0.0
        g = self._gs[name]
        rec = RecordingPen()
        g.draw(rec)
        s = size / self._upem
        pen = SVGPathPen(self._gs)
        rec.replay(TransformPen(pen, (s, 0, 0, -s, x, y)))
        return pen.getCommands(), g.width * s

    def render(self, text: str, size: float, x: float, y: float, *,
               ls: float = 0, fill: str = "#000", fill_opacity: str = "",
               anchor: str = "start") -> tuple[list[str], float]:
        advs = [self._glyph_path(c, size, 0, 0)[1] for c in text]
        total = sum(advs) + ls * max(0, len(text) - 1)
        cx = x - total / 2 if anchor == "middle" else x
        paths: list[str] = []
        fo = f' fill-opacity="{fill_opacity}"' if fill_opacity else ""
        for i, ch in enumerate(text):
            d, _ = self._glyph_path(ch, size, cx, y)
            if d:
                paths.append(f'  <path d="{d}" fill="{fill}"{fo}/>')
            cx += advs[i] + ls
        return paths, cx


def main():
    r500 = _Renderer(500)
    r700 = _Renderer(700)
    r700_inter = _Renderer(700, FONT_INTER)
    r900 = _Renderer(900)

    svg: list[str] = []
    a = svg.append

    a('<svg xmlns="http://www.w3.org/2000/svg" width="1040" height="300"'
      ' viewBox="0 0 1040 300">')

    # bars + star (geometry — kept verbatim)
    a('<g transform="translate(7.61,30.59) scale(1.2439)">')
    a('  <rect x="39.5" y="146" width="13" height="22" rx="6" fill="#BA0C2F"/>')
    a('  <rect x="57.5" y="126" width="13" height="42" rx="6" fill="#BA0C2F"/>')
    a('  <rect x="75.5" y="106" width="13" height="62" rx="6" fill="#BA0C2F"/>')
    a('  <rect x="93.5" y="78"  width="13" height="90" rx="6" fill="#16294E"/>')
    a('  <rect x="111.5" y="106" width="13" height="62" rx="6" fill="#BA0C2F"/>')
    a('  <rect x="129.5" y="126" width="13" height="42" rx="6" fill="#BA0C2F"/>')
    a('  <rect x="147.5" y="146" width="13" height="22" rx="6" fill="#BA0C2F"/>')
    a('  <path d="M100,27 L103.8,42.2 L119,46 L103.8,49.8'
      ' L100,65 L96.2,49.8 L81,46 L96.2,42.2 Z" fill="#B6892B"/>')
    a('</g>')

    # divider
    a('<line x1="262" y1="72" x2="262" y2="240"'
      ' stroke="#16294E" stroke-opacity="0.3" stroke-width="2"/>')

    # line 1: 國立臺灣大學 ｜ NTU
    p1, ex = r500.render("國立臺灣大學", 22, 292, 96, ls=5, fill="#6B7280")
    p_sep, ex2 = r500.render("｜", 22, ex + 16, 96,
                              fill="#16294E", fill_opacity="0.3")
    p_ntu, _ = r700_inter.render("NTU", 22, ex2 + 10, 96, ls=3, fill="#6B7280")
    svg.extend(p1 + p_sep + p_ntu)

    # line 2: 北區高中學生科學研究
    p2, _ = r900.render("北區高中學生科學研究", 40, 290, 160, ls=2, fill="#16294E")
    svg.extend(p2)

    # line 3: 人才培育計畫
    p3, _ = r900.render("人才培育計畫", 40, 290, 210, ls=2, fill="#16294E")
    svg.extend(p3)

    # pill
    a('<rect x="290" y="230" width="156" height="42" rx="6" fill="#BA0C2F"/>')

    # 數學組 (centered in pill)
    p4, _ = r700.render("數學組", 24, 372, 259, ls=8, fill="#FFFFFF",
                         anchor="middle")
    svg.extend(p4)

    a("</svg>")

    r500.close(); r700.close(); r700_inter.close(); r900.close()

    OUT.write_text("\n".join(svg), encoding="utf-8")
    print(f"wrote {OUT}  ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
