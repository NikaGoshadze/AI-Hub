import pytest

from pizza_app.chat_summary import summary_lines


def test_summary_lines_missing_and_empty():
    assert summary_lines(None) == ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]
    assert summary_lines("") == ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]


def test_summary_lines_populated_preserves_formatting():
    assert summary_lines("მოკლე ისტორია") == [
        "\n--- მიმდინარე საუბრის ისტორია ---",
        "მოკლე ისტორია",
    ]
