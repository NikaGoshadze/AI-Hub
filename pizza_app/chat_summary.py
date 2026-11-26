"""Pure helpers for rendering the chat summary output."""


def summary_lines(summary):
    """Return the exact lines to print for the summary command.

    Treat None and the empty string identically, preserving the existing
    Georgian system message and leading newline behavior.
    """
    if not summary:
        return "\n[System: ჯერ საუბრის ისტორია არ არის.]"
    return "\n--- მიმდინარე საუბრის ისტორია ---\n" + summary
