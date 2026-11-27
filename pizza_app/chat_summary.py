"""Pure formatting helpers for the pizza app conversation summary."""


def summary_lines(summary: str | None):
    """Return the printable lines for the current conversation summary.

    Missing, empty, and other falsy values all produce the same system line.
    """
    if not summary:
        return ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]

    return ["\n--- მიმდინარე საუბრის ისტორია ---", summary]
