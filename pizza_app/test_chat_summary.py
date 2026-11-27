from pizza_app.chat_summary import summary_lines


def test_summary_lines_missing_summary_returns_no_history_message():
    assert summary_lines(None) == ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]


def test_summary_lines_empty_summary_returns_no_history_message():
    assert summary_lines("") == ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]


def test_summary_lines_populated_summary_returns_heading_and_summary():
    assert summary_lines("პიცა: მარგარიტა\nსასმელი: წყალი") == [
        "\n--- მიმდინარე საუბრის ისტორია ---",
        "პიცა: მარგარიტა\nსასმელი: წყალი",
    ]
