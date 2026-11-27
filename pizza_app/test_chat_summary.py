import unittest

from pizza_app.chat_summary import summary_lines


class SummaryLinesTests(unittest.TestCase):
    def test_missing_summary_uses_no_history_message(self):
        self.assertEqual(
            summary_lines(None),
            ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]
        )

    def test_empty_summary_uses_no_history_message(self):
        self.assertEqual(
            summary_lines(""),
            ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]
        )

    def test_populated_summary_returns_header_and_summary(self):
        self.assertEqual(
            summary_lines("საუბრის შეჯამება"),
            ["\n--- მიმდინარე საუბრის ისტორია ---", "საუბრის შეჯამება"]
        )


if __name__ == "__main__":
    unittest.main()
