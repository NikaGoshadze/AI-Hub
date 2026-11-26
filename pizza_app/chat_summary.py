"""Pure helper for formatting chat summary output."""


def summary_lines(summary):
    """Return the lines to print for the summary command.

    Falsy summaries use the existing fallback message.
    """
    if not summary:
        return ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]

    return ["\n--- მიმდინარე საუბრის ისტორია ---", summary]
