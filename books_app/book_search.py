from dataclasses import dataclass


@dataclass(frozen=True)
class BookSearchResult:
    title: str
    authors: str


def lookup_books(query: str, vectorstore, limit: int = 3) -> tuple[list[BookSearchResult], int]:
    results = vectorstore.similarity_search(query, k=limit)
    structured_results = [
        BookSearchResult(
            title=doc.metadata.get('title', 'N/A'),
            authors=doc.metadata.get('authors', 'N/A')
        )
        for doc in results
    ]
    return structured_results, len(structured_results)


def search_books(query: str, vectorstore, limit: int = 3) -> str:
    results, _ = lookup_books(query, vectorstore, limit=limit)
    if not results:
        return "No relevant books found in the database."
    
    response_string = "Found the following relevant books in the database:\n"
    for doc in results:
        response_string += f"- Title: {doc.title}, Authors: {doc.authors}\n"
    return response_string
