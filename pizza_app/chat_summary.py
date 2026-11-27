"""Pure helpers for rendering chat summary output."""

from __future__ import annotations


def summary_lines(summary: str | None) -> list[str]:
    """Return the exact CLI lines for the current summary state."""
    if not summary:
        return ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]

    return ["\n--- მიმდინარე საუბრის ისტორია ---", summary]
