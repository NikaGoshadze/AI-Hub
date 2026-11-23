def _normalize_authors(value):
    if isinstance(value, (list, tuple, set)):
        return ", ".join(str(item) for item in value)
    return value if value is not None else "N/A"


def _get_metadata_value(metadata, key, default="N/A"):
    if not metadata:
        return default
    return metadata.get(key, default)


def _match_author_filter(doc, author_filter: str) -> bool:
    if not author_filter:
        return True
    metadata = getattr(doc, "metadata", {}) or {}
    authors = _get_metadata_value(metadata, "authors", "")
    return author_filter.lower() in str(authors).lower()


def get_book_search_results(query: str, vectorstore, author_filter: str = ""):
    results = vectorstore.similarity_search(query, k=3)
    filtered_results = [doc for doc in results if _match_author_filter(doc, author_filter)]
    return filtered_results


def search_books(query: str, vectorstore) -> str:
    results = get_book_search_results(query, vectorstore)
    if not results:
        return "No relevant books found in the database."
    
    response_string = "Found the following relevant books in the database:\n"
    for doc in results:
        title = doc.metadata.get('title', 'N/A')
        authors = doc.metadata.get('authors', 'N/A')
        response_string += f"- Title: {title}, Authors: {authors}\n"
    return response_string
