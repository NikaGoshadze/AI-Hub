from __future__ import annotations

from typing import Any, Dict, List, Optional


def _format_results(results) -> str:
    if not results:
        return "No relevant books found in the database."

    response_string = "Found the following relevant books in the database:\n"
    for doc in results:
        title = doc.metadata.get("title", "N/A")
        authors = doc.metadata.get("authors", "N/A")
        response_string += f"- Title: {title}, Authors: {authors}\n"
    return response_string


def _search_vectorstore(query: str, vectorstore, author_filter: str = "", count: int = 3):
    search_kwargs: Dict[str, Any] = {"k": count}
    if author_filter:
        search_kwargs["filter"] = {"authors": author_filter}
    return vectorstore.similarity_search(query, **search_kwargs)


def search_books(query: str, vectorstore, author_filter: str = "", count: int = 3) -> str:
    results = _search_vectorstore(query, vectorstore, author_filter=author_filter, count=count)
    return _format_results(results)


def search_books_structured(
    query: str,
    vectorstore,
    author_filter: str = "",
    count: int = 3,
) -> List[Dict[str, Any]]:
    results = _search_vectorstore(query, vectorstore, author_filter=author_filter, count=count)
    structured_results: List[Dict[str, Any]] = []
    for doc in results:
        metadata = getattr(doc, "metadata", {}) or {}
        structured_results.append(
            {
                "title": metadata.get("title"),
                "authors": metadata.get("authors"),
                "metadata": metadata,
            }
        )
    return structured_results
