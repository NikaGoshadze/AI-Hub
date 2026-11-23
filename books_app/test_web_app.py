import importlib
import sys
from types import SimpleNamespace
from unittest.mock import Mock

import pytest


@pytest.fixture()
def web_app_module(monkeypatch):
    fake_main = SimpleNamespace(search_book_database=Mock())
    monkeypatch.setitem(sys.modules, "books_app.main", fake_main)
    sys.modules.pop("books_app.web_app", None)
    module = importlib.import_module("books_app.web_app")
    yield module, fake_main.search_book_database
    sys.modules.pop("books_app.web_app", None)


def test_blank_query_shows_prompt_and_skips_search(web_app_module):
    module, search_mock = web_app_module
    client = module.app.test_client()

    response = client.post("/", data={"query": "   "})

    assert response.status_code == 200
    body = response.data.decode()
    assert "Please enter a search term to look for matching books." in body
    search_mock.assert_not_called()


def test_service_failure_shows_friendly_error(web_app_module):
    module, search_mock = web_app_module
    search_mock.side_effect = RuntimeError("Backend unavailable")
    client = module.app.test_client()

    response = client.post("/", data={"query": "example"})

    assert response.status_code == 200
    body = response.data.decode()
    assert "Sorry, the book search service is temporarily unavailable." in body
    assert "Search query" in body
    search_mock.assert_called_once_with("example")


def test_success_and_no_results_render_results(web_app_module):
    module, search_mock = web_app_module
    client = module.app.test_client()

    search_mock.return_value = "Found the following relevant books in the database:\n- Title: Example, Authors: Writer\n"
    response = client.post("/", data={"query": "example"})
    body = response.data.decode()
    assert response.status_code == 200
    assert "Found the following relevant books in the database:" in body
    assert "- Title: Example, Authors: Writer" in body

    search_mock.reset_mock()
    search_mock.return_value = "No relevant books found in the database."
    response = client.post("/", data={"query": "missing"})
    body = response.data.decode()
    assert response.status_code == 200
    assert "No relevant books found in the database." in body
    search_mock.assert_called_once_with("missing")
