from pizza_app.chat_commands import is_quit_or_exit_command, is_summary_command


def test_quit_and_exit_commands_match_case_insensitively():
    assert is_quit_or_exit_command("quit") is True
    assert is_quit_or_exit_command("exit") is True
    assert is_quit_or_exit_command("QuIt") is True
    assert is_quit_or_exit_command("ExIt") is True


def test_whitespace_is_preserved_and_does_not_newly_match():
    assert is_quit_or_exit_command(" quit") is False
    assert is_quit_or_exit_command("quit ") is False
    assert is_quit_or_exit_command("\tquit") is False
    assert is_quit_or_exit_command("exit\n") is False


def test_ordinary_non_command_input_is_false():
    assert is_quit_or_exit_command("hello") is False
    assert is_quit_or_exit_command("!summary") is False
    assert is_quit_or_exit_command("pizza order") is False


def test_summary_command_matches_case_insensitively():
    assert is_summary_command("!summary") is True
    assert is_summary_command("!SuMmArY") is True


def test_summary_command_rejects_whitespace_and_other_input():
    assert is_summary_command(" !summary") is False
    assert is_summary_command("!summary ") is False
    assert is_summary_command("summary") is False
    assert is_summary_command("hello") is False
