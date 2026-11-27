"""Pure summary formatting helpers for the pizza app."""


def summary_lines(summary: str | None) -> list[str]:
    """Return the exact lines for the !summary command output."""
    if not summary:
        return ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]

    return ["\n--- მიმდინარე საუბრის ისტორია ---", summary]
