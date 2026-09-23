"""build.py 的回歸測試（2026-09-23 程式碼審查 E 批）。

    python test_build.py

純 stdlib unittest。兩層：
  - **stub 層**（永遠跑）：把 build.subprocess.run 換成假的——latexmk 寫出指定的 log 與一份
    假 PDF、字形閘回指定的 (rc, stdout, stderr)——再真的呼叫 build.build()，斷言它 FAIL／
    PASS、印了什麼、PDF 有沒有進 dist。HERE／UNITS 指到暫存資料夾，不碰版控中的 dist/。
  - **實跑層**（有 latexmk 才跑）：用迷你 .tex 真的跑 latexmk，驗 log 格式與互動模式的假設。

  - E-02（`RefCheckTest`）：log 有 undefined reference／multiply defined label 就 FAIL 並列出 key。
"""
import contextlib
import io
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build  # noqa: E402

CLEAN_LOG = """This is LuaHBTeX, Version 1.24.0 (MiKTeX 26.2)
(./x.tex
LaTeX2e <2025-11-01>
[1]
Output written on x.pdf (1 page, 6553 bytes).
Transcript written on x.log.
"""
GLYPH_PASS = (0, "  NewCM10-Regular  10 字形 → 0 個輪廓不符\n\n字形閘 PASS：10 個嵌入字形的輪廓全數符合其 CID\n", "")


class FakeRun:
    """build.subprocess.run 的替身：latexmk → 寫 log＋假 PDF；check_glyphs → 回 `glyph`。"""

    def __init__(self, root, log=CLEAN_LOG, latexmk=(0, "", ""), glyph=GLYPH_PASS):
        self.root, self.log, self.latexmk, self.glyph = root, log, latexmk, glyph
        self.calls = []

    def __call__(self, args, **kw):
        self.calls.append((list(args), kw))
        if args[0] == "latexmk":
            aux = self.root / "build" / "aux-x"
            aux.mkdir(parents=True, exist_ok=True)
            (aux / "x.log").write_text(self.log, encoding="utf-8")
            (self.root / "src" / "x" / "x.pdf").write_bytes(b"%PDF-1.4 stub")
            return subprocess.CompletedProcess(args, *self.latexmk)
        return subprocess.CompletedProcess(args, *self.glyph)


class StubBuild(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        (self.tmp / "src" / "x").mkdir(parents=True)
        (self.tmp / "src" / "x" / "x.tex").write_text("% stub\n", encoding="utf-8")

    def build(self, **fake_kw):
        """跑 build.build('x')；回 (exit code 或 None, 印出的文字, dist PDF 是否存在, FakeRun)。"""
        fake = FakeRun(self.tmp, **fake_kw)
        out = io.StringIO()
        code = None
        with mock.patch.object(build, "HERE", self.tmp), \
                mock.patch.object(build, "UNITS", {"x": "x"}), \
                mock.patch.object(build.subprocess, "run", fake), \
                contextlib.redirect_stdout(out):
            try:
                build.build("x")
            except SystemExit as e:
                code = e.code
        return code, out.getvalue(), (self.tmp / "dist" / "x" / "x.pdf").exists(), fake


def wrap79(text):
    """TeX 的 log 在 max_print_line＝79 字元處硬斷行（MiKTeX 實測）。"""
    return "\n".join(text[i:i + 79] for i in range(0, len(text), 79))


class RefCheckTest(StubBuild):
    """E-02：latexmk 碰到 undefined reference 時 rc=0，build.py 以前照樣 PASS 並把印著 ?? 的 PDF 送進 dist。"""

    def test_clean_log_passes(self):
        """護欄：乾淨的 log 仍 PASS、PDF 進 dist。"""
        code, out, in_dist, _ = self.build()
        self.assertIsNone(code, out)
        self.assertTrue(in_dist)
        self.assertIn("PASS", out)

    def test_undefined_reference_fails_and_names_key(self):
        log = CLEAN_LOG + (
            "\nLaTeX Warning: Reference `thm:nope' on page 1 undefined on input line 3.\n\n"
            "\nLaTeX Warning: There were undefined references.\n\n")
        code, out, in_dist, _ = self.build(log=log)
        self.assertEqual(code, 1, out)
        self.assertIn("thm:nope", out)
        self.assertFalse(in_dist, "帶 ?? 的 PDF 不得進 dist")

    def test_multiply_defined_label_fails_and_names_key(self):
        log = CLEAN_LOG + (
            "\nLaTeX Warning: Label `sec:a' multiply defined.\n\n"
            "\nLaTeX Warning: There were multiply-defined labels.\n\n")
        code, out, in_dist, _ = self.build(log=log)
        self.assertEqual(code, 1, out)
        self.assertIn("sec:a", out)
        self.assertFalse(in_dist)

    def test_wrapped_warning_key_is_recovered(self):
        """長 key 的 warning 會被 TeX 在 79 字元處切成兩行；key 要接回來完整列出。"""
        key = "thm:mean-value-theorem-for-definite-integrals"
        log = CLEAN_LOG + "\n" + wrap79(
            f"LaTeX Warning: Reference `{key}' on page 123 undefined on input line 456.") + "\n\n"
        log += "\nLaTeX Warning: There were undefined references.\n\n"
        code, out, _, _ = self.build(log=log)
        self.assertEqual(code, 1, out)
        self.assertIn(key, out)

    def test_summary_line_alone_still_fails(self):
        """抓不到 key（格式變了）也不得放行：摘要行本身就是 FAIL 的依據。"""
        log = CLEAN_LOG + "\nLaTeX Warning: There were undefined references.\n\n"
        code, out, in_dist, _ = self.build(log=log)
        self.assertEqual(code, 1, out)
        self.assertFalse(in_dist)


@unittest.skipUnless(shutil.which("latexmk"), "需要 latexmk（MiKTeX）")
class RealLatexmkTest(unittest.TestCase):
    """實跑 latexmk：log 格式與 stub 的假設一致（審查員 undef_repro 的測試化）。"""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        shutil.copy(HERE / "check_glyphs.py", self.tmp / "check_glyphs.py")

    def unit(self, name, body):
        d = self.tmp / "src" / name
        d.mkdir(parents=True)
        (d / f"{name}.tex").write_text(
            "\\documentclass{article}\n\\begin{document}\n" + body + "\n\\end{document}\n", encoding="utf-8")

    def test_undefined_reference_real_log(self):
        self.unit("x", "Hello, see Theorem~\\ref{thm:nope} and a label\\label{sec:a} \\ref{sec:a}.")
        out = io.StringIO()
        code = None
        with mock.patch.object(build, "HERE", self.tmp), mock.patch.object(build, "UNITS", {"x": "x"}), \
                contextlib.redirect_stdout(out):
            try:
                build.build("x")
            except SystemExit as e:
                code = e.code
        self.assertEqual(code, 1, out.getvalue())
        self.assertIn("thm:nope", out.getvalue())
        self.assertNotIn("sec:a", out.getvalue(), "sec:a 第二輪已解析，只該列最後一輪 log 的 key")
        self.assertFalse((self.tmp / "dist" / "x" / "x.pdf").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
