"""Pure helpers for rendering chat summary output."""


def summary_lines(current_summary: str | None):
    """Return the exact print lines for the summary display.

    Missing or empty summaries produce the same output.
    """
    if not current_summary:
        return ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]

    return ["\n--- მიმდინარე საუბრის ისტორია ---", current_summary]
