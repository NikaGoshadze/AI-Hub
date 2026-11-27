"""Pure summary formatting helpers for the pizza app."""


def summary_lines(summary_text):
    """Return the exact lines printed for the summary command.

    Treat missing and empty summary text the same way, preserving the current
    Georgian messages and leading newline formatting.
    """
    if not summary_text:
        return ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]

    return ["\n--- მიმდინარე საუბრის ისტორია ---", summary_text]
