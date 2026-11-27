"""Pure helpers for formatting the conversation summary output."""


def summary_lines(summary):
    """Return the exact printable lines for the summary command output."""
    if not summary:
        return ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]

    return ["\n--- მიმდინარე საუბრის ისტორია ---", summary]
