"""export_figs.mjs 的回歸測試（2026-09-23 程式碼審查 E-06）。

    python test_export_figs.py

純 stdlib unittest，需要 node。只驗一件事：**repo 放在含空白或中文的路徑下，圖匯出仍找得到
內附的 Inter**。以前 INTER_DIR 用 `new URL(".", import.meta.url).pathname` 組路徑，拿到的是
百分比編碼過的 URL 路徑（空白→%20、中文→%E4%B8%AD…），route() 因此誤報
「font not found … see TYPESETTING_GUIDE §9.1」後 exit 1，把人引去排查字型安裝。

做法：把 export_figs.mjs 與 template/fonts/inter/ 複製到含空白＋中文的暫存資料夾，CHROME 指向
一個不存在的 exe——字型檢查發生在 spawn Chrome 之前，所以「過了字型階段」的證據就是 spawn
失敗（ENOENT）而不是 font not found。不需要 Chrome、不連網。
"""
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent


@unittest.skipUnless(shutil.which("node"), "需要 node")
class InterDirPathTest(unittest.TestCase):
    def test_inter_found_under_space_and_cjk_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "with space 中文路徑"
            shutil.copytree(HERE / "template" / "fonts" / "inter", root / "template" / "fonts" / "inter")
            shutil.copy(HERE / "export_figs.mjs", root / "export_figs.mjs")
            r = subprocess.run(
                ["node", str(root / "export_figs.mjs"), str(root / "missing.html"), str(root / "out")],
                env={**os.environ, "CHROME": str(root / "no-such-chrome.exe")}, stdin=subprocess.DEVNULL,
                capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
        out = r.stdout + r.stderr
        self.assertNotIn("font not found", out)
        self.assertIn("ENOENT", out, "應該走到 spawn Chrome 那一步（字型階段已過）")


if __name__ == "__main__":
    unittest.main(verbosity=2)
