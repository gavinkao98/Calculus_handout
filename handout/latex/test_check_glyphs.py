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

2026-09-23 程式碼審查另補兩組：
  - E-01（`FontIdentityTest`）：Type 3 字型與沒嵌入的字型不得落在閘的視野外——Type 3 只准
    `FIG_TYPE3_OK` 具名白名單內的家族，名單外與沒嵌入的非 Type 3 字型一律 FAIL 並指名。
  - E-05（`FindOriginalTest`）：kpsewhich 的輸出以 UTF-8 解碼；TeX 樹路徑含中文時不得崩潰。
"""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import fitz

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import check_glyphs  # noqa: E402
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


def pdf_with_fonts(path, fonts):
    """一頁空白 PDF，頁面資源掛上 `fonts`＝[(Subtype, 名稱)]，全都**沒有** FontFile：
    Type3 帶 FontDescriptor（Chrome/Skia 嵌圖字型的形狀）、TrueType 帶 FontDescriptor 但沒
    FontFile2（沒嵌入）、Type1 連 descriptor 都沒有（標準 14 字型的寫法）。"""
    doc = fitz.open()
    page = doc.new_page()
    refs = []
    for i, (subtype, name) in enumerate(fonts):
        fd = None
        if subtype in ("Type3", "TrueType"):
            fd = doc.get_new_xref()
            doc.update_object(fd, f"<< /Type /FontDescriptor /FontName /{name} /Flags 4 >>")
        if subtype == "Type3":
            obj = (f"<< /Type /Font /Subtype /Type3 /FontDescriptor {fd} 0 R /FontBBox [0 0 1000 1000]"
                   " /FontMatrix [0.001 0 0 0.001 0 0] /CharProcs << >>"
                   " /Encoding << /Type /Encoding /Differences [] >> /FirstChar 0 /LastChar 0 /Widths [0] >>")
        elif subtype == "TrueType":
            obj = f"<< /Type /Font /Subtype /TrueType /BaseFont /{name} /FontDescriptor {fd} 0 R >>"
        else:
            obj = f"<< /Type /Font /Subtype /{subtype} /BaseFont /{name} >>"
        x = doc.get_new_xref()
        doc.update_object(x, obj)
        refs.append(f"/F{i} {x} 0 R")
    doc.xref_set_key(page.xref, "Resources", f"<< /Font << {' '.join(refs)} >> >>")
    doc.save(str(path))


class FontIdentityTest(unittest.TestCase):
    """E-01：沒有 FontFile 的字型（Type 3、沒嵌入的字型）也要過閘，不得無聲 PASS。"""

    def gate(self, fonts):
        with tempfile.TemporaryDirectory() as tmp:
            pdf = Path(tmp) / "f.pdf"
            pdf_with_fonts(pdf, fonts)
            r = subprocess.run([sys.executable, str(HERE / "check_glyphs.py"), str(pdf)],
                               capture_output=True, text=True, encoding="utf-8", errors="replace")
        return r.returncode, r.stdout + r.stderr

    def test_unlisted_type3_font_fails_and_is_named(self):
        """Chrome 把 variable 系統字型（Win10 的 Bahnschrift）嵌成 Type 3：要 FAIL 並指名。"""
        rc, out = self.gate([("Type3", "AAAAAA+Bahnschrift")])
        self.assertEqual(rc, 1, out)
        self.assertIn("Bahnschrift", out)

    def test_type3_system_cjk_fallback_fails(self):
        """審查員的重現：Type 3 名稱換成 JhengHei（ch02 退錯字型的那套）也要擋。"""
        rc, out = self.gate([("Type3", "AAAAAA+MicrosoftJhengHeiUIRegular")])
        self.assertEqual(rc, 1, out)
        self.assertIn("MicrosoftJhengHeiUIRegular", out)

    def test_type3_lookalike_family_is_not_listed(self):
        """白名單比的是家族：`Inter` 的前綴不得放行 `InterDisplay`。"""
        rc, out = self.gate([("Type3", "AAAAAA+InterDisplay-Regular")])
        self.assertEqual(rc, 1, out)
        self.assertIn("InterDisplay-Regular", out)

    def test_unembedded_truetype_fails_and_is_named(self):
        rc, out = self.gate([("TrueType", "Arial")])
        self.assertEqual(rc, 1, out)
        self.assertIn("Arial", out)

    def test_standard14_type1_without_descriptor_fails(self):
        rc, out = self.gate([("Type1", "Helvetica")])
        self.assertEqual(rc, 1, out)
        self.assertIn("Helvetica", out)

    def test_listed_type3_families_pass(self):
        """dist 裡實際出現的圖字型（2026-09-23 盤點 12 份 dist PDF）不得被誤擋。"""
        rc, out = self.gate([("Type3", "ABCDEF+Inter-Regular"), ("Type3", "ABCDEF+Inter"),
                             ("Type3", "ABCDEF+Inter-Italic"), ("Type3", "ABCDEF+mjx-ncm-n-Regular"),
                             ("Type3", "ABCDEF+mjx-ncm-zero-Regular")])
        self.assertEqual(rc, 0, out)
        self.assertIn("字形閘 PASS", out)


class FindOriginalTest(unittest.TestCase):
    """E-05：kpsewhich 的輸出是 UTF-8；用 locale（Windows 的 cp950）解碼，中文路徑就崩。"""

    def test_stdout_none_means_not_found(self):
        """解碼失敗時 subprocess 的 stdout 會是 None：當成找不到，不得 AttributeError。"""
        fake = subprocess.CompletedProcess(["kpsewhich"], 0, stdout=None, stderr=None)
        with mock.patch.object(check_glyphs.subprocess, "run", return_value=fake):
            self.assertIsNone(check_glyphs.find_original("ABCDEF+NoSuchFont-Regular"))

    @unittest.skipUnless(shutil.which("kpsewhich"), "需要 kpsewhich（MiKTeX）")
    def test_cjk_texmf_path_is_found(self):
        """TeX 樹在中文路徑下（使用者名稱含中文的 per-user MiKTeX）時仍找得到原始字型。"""
        real_run = subprocess.run
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "字型測試"
            d.mkdir()
            shutil.copy(HERE / "template" / "fonts" / "inter" / "Inter-Regular.otf", d / "ZZTest-Regular.otf")

            def run(args, **kw):             # 讓 kpsewhich 在中文資料夾裡找；其餘沿用 check_glyphs 的 kwargs
                if args and args[0] == "kpsewhich":
                    args = ["kpsewhich", f"-path={d}"] + args[1:]
                return real_run(args, **kw)

            with mock.patch.object(check_glyphs.subprocess, "run", run):
                found = check_glyphs.find_original("ABCDEF+ZZTest-Regular")
            self.assertIsNotNone(found)
            self.assertTrue(found.exists())
            self.assertEqual(found.resolve(), (d / "ZZTest-Regular.otf").resolve())


if __name__ == "__main__":
    unittest.main(verbosity=2)
