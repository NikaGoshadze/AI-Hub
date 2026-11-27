"""Pure helpers for rendering pizza chat summary output."""


from __future__ import annotations


def summary_lines(current_summary):
    """Return the printable lines for the summary command.

    Missing and empty summaries are treated identically.
    """
    if not current_summary:
        return ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]
    return ["\n--- მიმდინარე საუბრის ისტორია ---", current_summary]
