from pizza_app.chat_summary import summary_lines


def test_summary_lines_for_missing_summary() -> None:
    assert summary_lines(None) == ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]


def test_summary_lines_for_empty_summary() -> None:
    assert summary_lines("") == ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]


def test_summary_lines_for_populated_summary() -> None:
    assert summary_lines("პირველი შეკვეთა: მარგერიტა") == [
        "\n--- მიმდინარე საუბრის ისტორია ---",
        "პირველი შეკვეთა: მარგერიტა",
    ]
