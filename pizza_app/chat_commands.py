"""Pure chat command helpers for the pizza app."""


def is_quit_or_exit_command(text: str) -> bool:
    """Return True for quit/exit commands, matching case-insensitively.

    This preserves the current whitespace behavior exactly by avoiding any
    stripping or normalization beyond lowercasing.
    """
    return text.lower() in ("quit", "exit")


def is_summary_command(text: str) -> bool:
    """Return True for the summary command, matching case-insensitively.

    This preserves the current whitespace behavior exactly by avoiding any
    stripping or normalization beyond lowercasing.
    """
    return text.lower() == "!summary"
