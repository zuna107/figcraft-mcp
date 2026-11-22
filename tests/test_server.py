import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from figcraft_mcp import (
    ANTI_SLOP_TOKENS,
    BANNED_PATTERNS,
    COMPONENT_RECIPES,
    ICON_BBOX,
    ICONS,
    STYLE_PRESETS,
    UNIVERSAL_HEURISTICS,
    icon_cmds,
    resolve_cli_path,
)
from figcraft_mcp.server import EXTRA_TOOLS, FigCraftMCPServer


class TestFigCraftMCPPackage(unittest.TestCase):
    def test_icons_and_bboxes_match(self):
        self.assertGreaterEqual(len(ICONS), 35)
        for key in ICONS:
            self.assertIn(key, ICON_BBOX, f"Missing precomputed bbox for icon '{key}'")
            cmds = icon_cmds(1, f"Icon {key}", key, 10, 20, 16, "#1E1E2D", 1.8)
            self.assertEqual(len(cmds), 2)
            self.assertEqual(cmds[0]["command"], "node.create")
            self.assertEqual(cmds[1]["command"], "node.set")

    def test_anti_slop_tokens_complete(self):
        self.assertIn("colors", ANTI_SLOP_TOKENS)
        self.assertEqual(ANTI_SLOP_TOKENS["colors"]["surface_primary"], "#FFFFFF")
        self.assertGreaterEqual(len(BANNED_PATTERNS), 5)
        self.assertIn("searchable_scrollable_dropdown", COMPONENT_RECIPES)
        self.assertGreaterEqual(len(UNIVERSAL_HEURISTICS), 4)
        self.assertIn("neutral_clean", STYLE_PRESETS)
        self.assertIn("ios_hig", STYLE_PRESETS)
        self.assertIn("material_m3", STYLE_PRESETS)
        self.assertIn("dark_modern", STYLE_PRESETS)

    def test_extra_mcp_tools_schema(self):
        names = [t["name"] for t in EXTRA_TOOLS]
        self.assertIn("list_screens", names)
        self.assertIn("find_nodes", names)
        self.assertIn("place_lucide_icon", names)
        self.assertIn("create_prototype_link", names)
        self.assertIn("get_anti_slop_guidelines", names)

    def test_batch_formatter_token_optimization(self):
        # Test compact summary formatting to verify token reduction
        server = FigCraftMCPServer.__new__(FigCraftMCPServer)
        raw_results = [{"id": 101, "name": "A", "type": "frame"}, {"id": 102, "name": "B", "type": "text"}]
        summary_res = server._format_batch_result(raw_results, verbose=False)
        self.assertIn("content", summary_res)
        import json
        data = json.loads(summary_res["content"][0]["text"])
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["created_count"], 2)
        self.assertEqual(data["root_id"], 101)
        self.assertEqual(data["created_ids"], [101, 102])

        # Test verbose flag preserves raw output
        verbose_res = server._format_batch_result(raw_results, verbose=True)
        raw_data = json.loads(verbose_res["content"][0]["text"])
        self.assertEqual(raw_data, raw_results)

    def test_cli_path_resolution(self):
        cli = resolve_cli_path()
        self.assertTrue(isinstance(cli, str) and len(cli) > 0)


if __name__ == "__main__":
    unittest.main()

