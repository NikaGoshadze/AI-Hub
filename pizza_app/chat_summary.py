"""Pure helpers for the pizza app conversation summary display."""


def summary_lines(summary):
    """Return the exact lines printed for the current conversation summary.

    An absent or empty summary maps to the current system line. A populated
    summary maps to the existing heading and summary body lines.
    """
    if not summary:
        return ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]

    return ["\n--- მიმდინარე საუბრის ისტორია ---", summary]
