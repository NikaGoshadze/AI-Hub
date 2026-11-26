"""Pure helpers for formatting chat summary output."""

from __future__ import annotations


def summary_lines(summary: str | None) -> list[str]:
    """Return the exact printable lines for the summary command."""
    if not summary:
        return ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]
    return ["\n--- მიმდინარე საუბრის ისტორია ---", summary]
