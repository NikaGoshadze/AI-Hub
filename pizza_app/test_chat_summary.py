import importlib.util
import pathlib
import sys
import types


def _load_chat_summary_module():
    path = pathlib.Path(__file__).with_name("chat_summary.py")
    spec = importlib.util.spec_from_file_location("pizza_app.chat_summary", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_summary_lines_missing_and_empty_match_no_history_message():
    chat_summary = _load_chat_summary_module()

    assert chat_summary.summary_lines(None) == ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]
    assert chat_summary.summary_lines("") == ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]


def test_summary_lines_populated_summary_returns_title_and_summary():
    chat_summary = _load_chat_summary_module()

    assert chat_summary.summary_lines("პიცის შეკვეთა დადასტურებულია") == [
        "\n--- მიმდინარე საუბრის ისტორია ---",
        "პიცის შეკვეთა დადასტურებულია",
    ]
