from pizza_app.chat_summary import summary_lines


def test_summary_lines_missing_uses_fallback_message():
    assert summary_lines(None) == ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]


def test_summary_lines_empty_uses_fallback_message():
    assert summary_lines("") == ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]


def test_summary_lines_populated_returns_header_and_summary():
    assert summary_lines("პიცა 1, სასმელი 2") == [
        "\n--- მიმდინარე საუბრის ისტორია ---",
        "პიცა 1, სასმელი 2",
    ]
