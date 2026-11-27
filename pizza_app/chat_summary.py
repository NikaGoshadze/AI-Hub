"""Pure formatting helpers for pizza app summary display."""


def summary_lines(current_summary):
    """Return the exact lines printed for the summary command.

    Treat falsy values as an empty summary state.
    """
    if not current_summary:
        return ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]

    return ["\n--- მიმდინარე საუბრის ისტორია ---", current_summary]
