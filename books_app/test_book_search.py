from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from books_app.book_search import search_books


def test_success():
    store = Mock()
    store.similarity_search.return_value = [
        SimpleNamespace(metadata={"title": "The Example", "authors": "A. Writer"})
    ]
    assert search_books("example", store) == (
        "Found the following relevant books in the database:\n"
        "- Title: The Example, Authors: A. Writer\n"
    )
    store.similarity_search.assert_called_once_with("example", k=3)


def test_empty():
    store = Mock()
    store.similarity_search.return_value = []
    assert search_books("missing", store) == "No relevant books found in the database."


def test_backend_error():
    store = Mock()
    store.similarity_search.side_effect = RuntimeError("Backend unavailable")
    with pytest.raises(RuntimeError, match="Backend unavailable"):
        search_books("example", store)
