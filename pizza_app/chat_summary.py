"""Pure chat summary helpers for the pizza app."""


def summary_lines(summary: str | None) -> list[str]:
    """Return the printable lines for the summary command."""
    if not summary:
        return ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]

    return ["\n--- მიმდინარე საუბრის ისტორია ---", summary]
