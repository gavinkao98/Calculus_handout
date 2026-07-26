"""check_glyphs.py 的回歸測試。

    python test_check_glyphs.py

純 stdlib unittest。本檔只守一件事：**輪廓比對器不得在合法的 TrueType 構造上崩掉，
也不得因為容錯而讓兩條不同的輪廓比成相等。**

緣起（2026-07-26，ch07 rollout）：`_glyf_outline` 假設 pen 吐出的每個點都是座標對，
於是遇到 `qCurveTo(p1…pn, None)` 就 `TypeError: 'NoneType' object is not iterable`。
那個 `None` 是 TrueType 的合法寫法——一整條輪廓全是 off-curve 點時，隱含的 on-curve
起點在相鄰兩點的中點，fontTools 的 pen protocol 用結尾的 `None` 表示。WebCM-Serif 的
`?`／`!`／`.`／`:`／`;`／`·` 等 68 個字形的圓點都是這樣畫的；ch07 是全書第一個把 `?`
帶進圖面板的單元，於是字形閘直接 crash（而不是回報 finding）。
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_glyphs import _glyf_outline  # noqa: E402


class FakeGlyph:
    """最小的 pen protocol 來源：把預錄的 (op, args) 重播給 pen。"""

    def __init__(self, ops):
        self.ops = ops

    def draw(self, pen):
        for op, args in self.ops:
            getattr(pen, op)(*args)


def gs(ops):
    return {"g": FakeGlyph(ops)}


# 一條全 off-curve 的閉合輪廓（圓點）：qCurveTo 以 None 結尾
ALL_OFF_CURVE = [
    ("moveTo", [(10.0, 20.0)]),
    ("qCurveTo", [(11.0, 21.0), (12.0, 22.0), (13.0, 23.0), (14.0, 24.0), None]),
    ("closePath", []),
]
# 同樣的點，但最後一點是實際的 on-curve 點而非隱含
LAST_POINT_EXPLICIT = [
    ("moveTo", [(10.0, 20.0)]),
    ("qCurveTo", [(11.0, 21.0), (12.0, 22.0), (13.0, 23.0), (14.0, 24.0)]),
    ("closePath", []),
]


class GlyfOutlineTest(unittest.TestCase):
    def test_all_off_curve_contour_does_not_crash(self):
        """ch07 的 `question`：qCurveTo 結尾的 None 不得讓比對器爆掉。"""
        self.assertTrue(_glyf_outline(gs(ALL_OFF_CURVE), "g"))

    def test_implied_oncurve_point_is_preserved(self):
        """None MUST 可區分——濾掉它等於在字形閘上開一個洞。"""
        self.assertNotEqual(
            _glyf_outline(gs(ALL_OFF_CURVE), "g"),
            _glyf_outline(gs(LAST_POINT_EXPLICIT), "g"),
        )

    def test_identical_outlines_still_compare_equal(self):
        """容錯不得破壞正常路徑：同一條輪廓仍須相等（含 None 的也一樣）。"""
        for ops in (ALL_OFF_CURVE, LAST_POINT_EXPLICIT):
            self.assertEqual(_glyf_outline(gs(ops), "g"), _glyf_outline(gs(ops), "g"))

    def test_coordinates_are_rounded_like_the_cff_path(self):
        """取整仍在（子集器的浮點噪音），且不因 None 的處理而失效。"""
        noisy = [("moveTo", [(10.04, 20.04)]), ("qCurveTo", [(11.04, 21.04), None])]
        clean = [("moveTo", [(10.0, 20.0)]), ("qCurveTo", [(11.0, 21.0), None])]
        self.assertEqual(_glyf_outline(gs(noisy), "g"), _glyf_outline(gs(clean), "g"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
