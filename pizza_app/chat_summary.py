"""Pure helpers for rendering chat summary output."""


def summary_lines(summary: str | None) -> list[str]:
    """Return the printable lines for the current conversation summary."""
    if not summary:
        return ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]

    return ["\n--- მიმდინარე საუბრის ისტორია ---", summary]
