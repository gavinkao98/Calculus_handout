"""離線報量回歸測試：無 API、模型、音檔或金鑰需求。"""
import ast
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

try:
    from . import tts_pilot_plan as planner
except ImportError:
    import tts_pilot_plan as planner


def fixture():
    storyboard = {"scenes": [{"id": name, "say": "中英 p q。 {show next} 回中心！"}
                              for name in ("mirror", "halfway", "recap")]}
    providers = []
    for provider, rule in (("minimax", "han_double"), ("eleven", "all_characters"), ("mimo", "free")):
        providers.append({"id": provider, "model": "model-1", "voice": "voice-1",
                          "voice_source": "https://example.org/voice", "parameters": {"speed": 1},
                          "billing": {"rule": rule, "unit_price": 0 if rule == "free" else 2,
                                      "per_units": 1000, "currency": "USD",
                                      "source": "https://example.org/price", "checked_on": "2026-09-26"}})
    return storyboard, {"version": 1, "scenes": [s["id"] for s in storyboard["scenes"]],
                        "glossary_revision": "v1", "providers": providers}


class PilotPlanTests(unittest.TestCase):
    def setUp(self):
        self.storyboard, self.config = fixture()

    def plan(self):
        return planner.build_plan(self.storyboard, self.config)

    def test_fixed_cap_and_pending_status(self):
        plan = self.plan()
        self.assertEqual(len(plan["requests"]), 9)
        self.assertEqual(plan["summary"]["hard_cap_requests"], 9)
        self.assertFalse(plan["summary"]["automatic_retry"])
        self.assertEqual(plan["approval"]["status"], "pending")
        self.assertEqual(plan["script_lock"]["status"], "pending")
        self.assertEqual(plan["script_lock"]["nfa_status"], "not_verified")
        self.assertEqual(plan["summary"]["reuse_count"], 0)
        self.assertEqual(plan["summary"]["take_registry"], "not_implemented")

    def test_whole_scene_and_punctuation_preserved(self):
        segment = self.plan()["segments"][0]
        self.assertEqual(segment["text"], "中英 p q。 回中心！")
        self.assertEqual(segment["characters"], 12)
        self.assertEqual(segment["nonwhitespace_characters"], 9)
        self.assertEqual(len(segment["cues"]), 2)

    def test_punctuation_changes_request_hash(self):
        before = self.plan()["requests"][0]["request_hash"]
        self.storyboard["scenes"][0]["say"] += "。"
        self.assertNotEqual(before, self.plan()["requests"][0]["request_hash"])

    def test_cue_change_only_changes_plan_hash(self):
        before = self.plan()
        self.storyboard["scenes"][0]["say"] = "中英 p q。 {show changed} 回中心！"
        after = self.plan()
        self.assertEqual(before["requests"][0]["request_hash"], after["requests"][0]["request_hash"])
        self.assertNotEqual(before["plan_snapshot_hash"], after["plan_snapshot_hash"])

    def test_cue_inside_word_does_not_add_space(self):
        for before, after, expected in (("回{show next}中心。", "回中{show next}心。", "回中心。"),
                                        ("mir{show next}ror!", "mirr{show next}or!", "mirror!")):
            with self.subTest(expected=expected):
                self.storyboard["scenes"][0]["say"] = before
                first = self.plan()
                self.storyboard["scenes"][0]["say"] = after
                second = self.plan()
                self.assertEqual(first["requests"][0]["request_hash"], second["requests"][0]["request_hash"])
                self.assertEqual(first["segments"][0]["text"], expected)

    def test_relative_absolute_source_path_snapshot_matches(self):
        path = Path(__file__).resolve().relative_to(Path.cwd())
        relative = planner.build_plan(self.storyboard, self.config, source_path=str(path))
        absolute = planner.build_plan(self.storyboard, self.config, source_path=str(path.resolve()))
        self.assertEqual(relative["plan_snapshot_hash"], absolute["plan_snapshot_hash"])
        self.assertEqual(relative["source_path"], Path(__file__).resolve().relative_to(planner.REPO_ROOT).as_posix())

    def test_glossary_revision_changes_plan_only(self):
        before = self.plan()
        self.config["glossary_revision"] = "v2"
        after = self.plan()
        self.assertEqual(before["requests"], after["requests"])
        self.assertNotEqual(before["plan_snapshot_hash"], after["plan_snapshot_hash"])

    def test_request_identity_includes_model_voice_parameters(self):
        for field, value in (("model", "other-model"), ("voice", "other-voice"), ("parameters", {"speed": 2})):
            with self.subTest(field=field):
                before = self.plan()["requests"][0]["request_hash"]
                self.config["providers"][0][field] = value
                self.assertNotEqual(before, self.plan()["requests"][0]["request_hash"])

    def test_unknown_and_duplicate_scenes_fail(self):
        for selected in (["missing", "halfway", "recap"], ["mirror", "mirror", "recap"]):
            with self.subTest(selected=selected):
                self.config["scenes"] = selected
                with self.assertRaises(ValueError):
                    self.plan()
        self.storyboard, self.config = fixture()
        self.storyboard["scenes"].append(copy.deepcopy(self.storyboard["scenes"][0]))
        with self.assertRaises(ValueError):
            self.plan()

    def test_wrong_scale_fails(self):
        self.config["providers"].pop()
        with self.assertRaises(ValueError):
            self.plan()

    def test_malformed_show_fails(self):
        for marker in ("{show}", "{show x", "{show x y}"):
            with self.subTest(marker=marker):
                self.storyboard["scenes"][0]["say"] = f"開始 {marker} 結束。"
                with self.assertRaises(ValueError):
                    self.plan()

    def test_unicode_spans_and_stable_cues(self):
        self.storyboard["scenes"][0]["say"] = "𠀀😀。{show first} p q。{show last}完。"
        segment = self.plan()["segments"][0]
        self.assertEqual(segment["cues"][0]["text_span"], [0, 3])
        for cue in segment["cues"]:
            start, end = cue["text_span"]
            self.assertEqual(segment["text"][start:end], cue["text"])
            start, end = cue["source_say_span"]
            self.assertEqual(" ".join(segment["source_say"][start:end].split()), cue["text"])
        self.assertEqual(segment["cues"][1]["cue_id"], "mirror.first")

    def test_empty_cues_and_repeated_reveals(self):
        self.storyboard["scenes"][0]["say"] = "{show x}{show x}字{show end}"
        segment = self.plan()["segments"][0]
        self.assertEqual([c["cue_id"] for c in segment["cues"]], ["mirror.x", "mirror.x.2", "mirror.end"])
        self.assertEqual(segment["cues"][-1]["text_span"], [1, 1])

    def test_mixed_duration_uncalibrated(self):
        result = planner.estimate_duration("中英𠀀 p q don't。")
        self.assertEqual(result["han_characters"], 3)
        self.assertEqual(result["english_words"], 3)
        self.assertEqual(result["seconds_range"], [1.6, 2.5])
        self.assertFalse(result["calibrated"])
        self.assertEqual(result["status"], "uncalibrated")

    def test_missing_price_voice_blockers(self):
        self.config["providers"][0]["voice"] = None
        self.config["providers"][0]["billing"]["unit_price"] = None
        result = self.plan()
        self.assertIn("minimax: 尚未選定 voice", result["blockers"])
        self.assertIn("minimax: 價格／計價基數／幣別未齊", result["blockers"])
        self.assertIsNone(result["providers"][0]["estimated_cost"])

    def test_billing_rules(self):
        result = self.plan()
        self.assertEqual([p["billing_units"] for p in result["providers"]], [51, 36, 36])
        self.assertEqual([p["estimated_cost"] for p in result["providers"]], [0.102, 0.072, 0.0])

    def test_html_escapes_all_source_values_and_includes_notes(self):
        hostile = '<script>alert("bad")</script>'
        self.storyboard["scenes"][0]["say"] += hostile
        self.config["providers"][0]["voice"] = hostile
        self.config["providers"][0]["billing"]["note"] = hostile
        self.config["preflight_notes"] = ["自訂前置說明", hostile]
        self.config["preflight_blockers"] = ["價格待核對"]
        result = self.plan()
        page = planner.render_html(result)
        self.assertNotIn("<script>", page)
        self.assertIn("&lt;script&gt;", page)
        self.assertIn("自訂前置說明", page)
        self.assertIn("價格待核對", result["blockers"])
        self.assertIn("沒有 live 執行能力", page)

    def test_baseline_remains_reference_only(self):
        self.config["calibration"] = {"measured_total_seconds": 76.26, "status": "baseline_reference_only"}
        result = self.plan()
        self.assertFalse(result["summary"]["duration_calibrated"])
        self.assertIn("76.26 秒", planner.render_html(result))

    def test_source_links_only_allow_http_schemes(self):
        page = planner.render_html(self.plan())
        self.assertIn('href="https://example.org/price"', page)
        self.config["providers"][0]["voice_source"] = 'javascript:alert("bad")'
        page = planner.render_html(self.plan())
        self.assertNotIn('href="javascript:', page)
        self.assertIn("javascript:alert(&quot;bad&quot;)", page)

    def test_cli_offline_without_environment_or_network(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            story, config, out_json, out_html = [root / name for name in ("story.yml", "config.json", "plan.json", "plan.html")]
            story.write_text(json.dumps(self.storyboard, ensure_ascii=False), encoding="utf-8")
            config.write_text(json.dumps(self.config), encoding="utf-8")
            with patch("socket.socket", side_effect=AssertionError("network forbidden")), patch("os.getenv", side_effect=AssertionError("env forbidden")):
                self.assertEqual(planner.main(["--storyboard", str(story), "--config", str(config), "--output-json", str(out_json), "--output-html", str(out_html)]), 0)
            result = json.loads(out_json.read_text(encoding="utf-8"))
            self.assertEqual(len(result["requests"]), 9)
            self.assertTrue(out_html.exists())
        tree = ast.parse(Path(planner.__file__).read_text(encoding="utf-8"))
        imports = {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)}
        imports |= {alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
        self.assertFalse(imports & {"os", "requests", "socket", "httpx", "tts", "pipeline.tts"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
