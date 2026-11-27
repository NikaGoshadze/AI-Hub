"""Pure chat summary formatting helpers for the pizza app."""


def summary_lines(summary):
    """Return the print-ready lines for the chat summary branch."""
    if not summary:
        return "\n[System: ჯერ საუბრის ისტორია არ არის.]"

    return "\n--- მიმდინარე საუბრის ისტორია ---\n" + summary