import unittest
from datetime import datetime
from types import SimpleNamespace
from unittest.mock import Mock, patch

import ptt_stock_digest as digest
from PyPtt import _api_get_post


class PttCompatibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bot = digest.create_ptt_bot()  # Initializes parsing; no connection.

    def test_new_article_layout_parses_body_and_comments(self):
        raw = (
            " 作者  reader (Reader) 看板  Stock\n"
            " 標題  [情報] 測試資料\n"
            " 時間  Wed Nov 11 21:46:10 2026\n"
            " ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ \n"
            "內文測試。\n--\n"
            " ※  發信站: 批踢踢實業坊(ptt.cc), 來自: 192.0.2.1 (臺灣)\n"
            " ※  文章網址: https://www.ptt.cc/bbs/Stock/M.1794404773.A.D4B.html\n"
            "推 reader: 這是有資訊量的推文內容 11/11 22:00\n"
        )
        post = _api_get_post._parse_post_content(
            self.bot, {"pass_format_check": False}, "Stock",
            digest.normalize_ptt_screen(raw),
        )
        self.assertTrue(post["pass_format_check"])
        self.assertIn("內文測試。", post["content"])
        self.assertEqual(len(post["comments"]), 1)
        self.assertIn("有資訊量", post["comments"][0]["content"])

    def test_article_info_box_keeps_source_url(self):
        screen = (
            "┌─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┐\n"
            "│ 文章網址: https://www.ptt.cc/bbs/Stock/M.1.A.123.html │\n"
            "└─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┘"
        )
        normalized = digest.normalize_ptt_screen(screen)
        self.assertIn("┌──", normalized)
        self.assertIn("└──", normalized)
        self.assertIn("https://www.ptt.cc/bbs/Stock/M.1.A.123.html", normalized)
        body = "正文中的分隔線\n ─ ─ ─ ─ ─ ─ ─ \n後文"
        self.assertEqual(digest.normalize_ptt_screen(body), body)

    def test_wrong_board_is_rejected_before_caching(self):
        bot = SimpleNamespace(
            connect_core=SimpleNamespace(
                get_screen_queue=lambda: ["看板《Other》\n文章列表"]
            )
        )
        with patch.object(digest._api_util, "goto_board"):
            with self.assertRaisesRegex(RuntimeError, "無法確認"):
                digest.prepare_read_only_board(bot, "Stock")

    def test_failed_reads_are_not_reported_as_no_popular_posts(self):
        bot = SimpleNamespace(
            get_newest_index=lambda *args: 3,
            get_post=Mock(return_value={"pass_format_check": False}),
        )
        with patch.object(digest, "prepare_read_only_board"):
            with self.assertRaisesRegex(RuntimeError, "全部讀取失敗"):
                digest.fetch_recent_posts(
                    bot, "Stock", datetime(2026, 11, 11),
                    datetime(2026, 11, 12), 50, 3, 1200, 12,
                )


if __name__ == "__main__":
    unittest.main()
