"""Pure helpers for rendering chat summary output."""


def summary_lines(current_summary):
    """Return printable lines for the current summary state."""
    if not current_summary:
        return ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]

    return ["\n--- მიმდინარე საუბრის ისტორია ---", current_summary]
