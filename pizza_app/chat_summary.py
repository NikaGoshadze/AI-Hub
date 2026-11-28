"""Pure chat summary helpers for the pizza app."""


def summary_lines(current_summary):
    """Return the lines to print for the current conversation summary.

    Missing and empty summaries are handled identically. Populated summaries
    preserve the current Georgian wording and leading newline behavior.
    """
    if not current_summary:
        return ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]

    return ["\n--- მიმდინარე საუბრის ისტორია ---", current_summary]
