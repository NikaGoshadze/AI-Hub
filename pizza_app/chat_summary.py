"""Pure helpers for formatting the pizza app summary display."""


def summary_lines(summary):
    """Return the printable lines for the summary command.

    Missing and empty summaries are treated the same and show the same
    one-line system message output.
    """
    if not summary:
        return ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]

    return ["\n--- მიმდინარე საუბრის ისტორია ---", summary]
