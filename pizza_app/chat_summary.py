"""Pure helpers for rendering chat summary output."""


def summary_lines(current_summary):
    """Return the printable lines for the `!summary` command.

    Missing and empty summary values are treated the same.
    """
    if not current_summary:
        return ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]

    return ["\n--- მიმდინარე საუბრის ისტორია ---", current_summary]
