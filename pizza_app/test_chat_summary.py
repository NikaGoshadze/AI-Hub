from pizza_app.chat_summary import summary_lines


def test_summary_lines_missing_summary():
    assert summary_lines(None) == ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]


def test_summary_lines_empty_summary():
    assert summary_lines("") == ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]


def test_summary_lines_populated_summary():
    summary = "გუშინ შეკვეთა იყო პეპერონი პიცა."
    assert summary_lines(summary) == ["\n--- მიმდინარე საუბრის ისტორია ---", summary]
