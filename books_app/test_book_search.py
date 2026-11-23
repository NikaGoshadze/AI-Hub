from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from books_app.book_search import lookup_books, search_books


def test_success():
    store = Mock()
    store.similarity_search.return_value = [
        SimpleNamespace(metadata={"title": "The Example", "authors": "A. Writer"})
    ]
    assert search_books("example", store, limit=5) == (
        "Found the following relevant books in the database:\n"
        "- Title: The Example, Authors: A. Writer\n"
    )
    store.similarity_search.assert_called_once_with("example", k=5)


def test_empty():
    store = Mock()
    store.similarity_search.return_value = []
    assert search_books("missing", store) == "No relevant books found in the database."


def test_lookup_books_returns_structured_results_and_count():
    store = Mock()
    store.similarity_search.return_value = [
        SimpleNamespace(metadata={"title": "First", "authors": "One"}),
        SimpleNamespace(metadata={"title": "Second", "authors": "Two"}),
    ]

    results, count = lookup_books("example", store, limit=2)

    assert count == 2
    assert results[0].title == "First"
    assert results[0].authors == "One"
    assert results[1].title == "Second"
    assert results[1].authors == "Two"
    store.similarity_search.assert_called_once_with("example", k=2)


def test_backend_error():
    store = Mock()
    store.similarity_search.side_effect = RuntimeError("Backend unavailable")
    with pytest.raises(RuntimeError, match="Backend unavailable"):
        search_books("example", store)
