"""Pure helpers for summary display formatting."""


def summary_lines(summary):
    """Return the lines that should be printed for the current summary."""
    if not summary:
        return ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]

    return ["\n--- მიმდინარე საუბრის ისტორია ---", summary]
