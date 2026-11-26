"""Pure summary display helpers for the pizza app."""


def summary_lines(current_summary):
    """Return the exact lines to print for the summary command."""
    if not current_summary:
        return ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]

    return ["\n--- მიმდინარე საუბრის ისტორია ---", current_summary]
