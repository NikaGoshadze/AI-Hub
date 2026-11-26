"""Pure chat summary helpers for the pizza app."""


def summary_lines(current_summary):
    """Return the exact printable lines for the summary command.

    This preserves the current falsy-check behavior exactly by treating None
    and empty strings as missing summary values without stripping or
    reformatting populated summaries.
    """
    if not current_summary:
        return ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]

    return ["\n--- მიმდინარე საუბრის ისტორია ---", current_summary]
