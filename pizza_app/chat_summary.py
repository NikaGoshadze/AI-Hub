"""Pure helpers for rendering chat summary output."""


def summary_lines(summary):
    """Return the display lines for the current conversation summary.

    Missing and explicitly empty summaries are treated the same.
    """
    if not summary:
        return ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]

    return ["\n--- მიმდინარე საუბრის ისტორია ---", summary]
