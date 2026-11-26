"""Pure chat summary formatting helpers for the pizza app."""


def summary_lines(summary: str | None) -> list[str]:
    """Return the printable lines for the summary command.

    Missing and empty summary content are treated the same way.
    """
    if not summary:
        return ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]

    return ["\n--- მიმდინარე საუბრის ისტორია ---", summary]
