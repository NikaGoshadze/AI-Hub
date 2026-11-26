import pytest

from pizza_app.chat_summary import summary_lines


@pytest.mark.parametrize(
    "summary,expected",
    [
        (None, ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]),
        ("", ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]),
        (
            "User ordered margherita pizza.",
            ["\n--- მიმდინარე საუბრის ისტორია ---", "User ordered margherita pizza."],
        ),
    ],
)
def test_summary_lines(summary, expected):
    assert summary_lines(summary) == expected
