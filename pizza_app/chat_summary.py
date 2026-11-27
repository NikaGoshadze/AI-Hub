"""Pure helpers for rendering chat summary output."""

from typing import Optional


def summary_lines(summary: Optional[str]) -> list[str]:
    """Return the exact lines printed for the summary command.

    Missing and empty summaries produce the same no-history message.
    """
    if not summary:
        return ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]

    return ["\n--- მიმდინარე საუბრის ისტორია ---", summary]
