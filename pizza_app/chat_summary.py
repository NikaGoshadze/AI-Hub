"""Pure helpers for presenting chat summaries."""


def summary_lines(summary):
    """Return the printable lines for the current chat summary."""
    if not summary:
        return ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]

    return ["\n--- მიმდინარე საუბრის ისტორია ---", summary]
