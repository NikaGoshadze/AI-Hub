"""Pure summary rendering helpers for the pizza app."""


def summary_lines(summary):
    """Return the exact console lines for the current summary state."""
    if not summary:
        return ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]

    return ["\n--- მიმდინარე საუბრის ისტორია ---", summary]
