from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest


@pytest.fixture()
def client():
    with patch("books_app.web_app.get_vectorstore") as get_vectorstore:
        store = Mock()
        get_vectorstore.return_value = store
        from books_app.web_app import app

        app.config.update(TESTING=True)
        with app.test_client() as test_client:
            yield test_client, store


def test_browser_search_returns_structured_results(client):
    test_client, store = client
    store.similarity_search.return_value = [
        SimpleNamespace(metadata={"title": "The Example", "authors": "A. Writer"}),
    ]

    response = test_client.post(
        "/search",
        data={"query": "example", "author_filter": "A. Writer", "count": "2"},
    )

    assert response.status_code == 200
    assert response.get_json() == {
        "status": "success",
        "results": [{"title": "The Example", "authors": "A. Writer", "metadata": {"title": "The Example", "authors": "A. Writer"}}],
    }
    store.similarity_search.assert_called_once_with(
        "example", k=2, filter={"authors": "A. Writer"}
    )


def test_browser_search_empty_results(client):
    test_client, store = client
    store.similarity_search.return_value = []

    response = test_client.post(
        "/search",
        data={"query": "missing", "count": "3"},
    )

    assert response.status_code == 200
    assert response.get_json() == {
        "status": "empty",
        "message": "No relevant books found in the database.",
        "results": [],
    }


def test_browser_search_backend_error(client):
    test_client, store = client
    store.similarity_search.side_effect = RuntimeError("Backend unavailable")

    response = test_client.post(
        "/search",
        data={"query": "example", "count": "1"},
    )

    assert response.status_code == 503
    assert response.get_json() == {
        "status": "error",
        "message": "The book search service is temporarily unavailable. Please try again later.",
        "results": [],
    }


def test_browser_search_rejects_invalid_count(client):
    test_client, _ = client

    response = test_client.post(
        "/search",
        data={"query": "example", "count": "not-a-number"},
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "status": "error",
        "message": "Result count must be a whole number.",
    }
