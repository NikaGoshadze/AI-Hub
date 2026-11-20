def search_books(query: str, vectorstore) -> str:
    results = vectorstore.similarity_search(query, k=3)
    if not results:
        return "No relevant books found in the database."
    
    response_string = "Found the following relevant books in the database:\n"
    for doc in results:
        title = doc.metadata.get('title', 'N/A')
        authors = doc.metadata.get('authors', 'N/A')
        response_string += f"- Title: {title}, Authors: {authors}\n"
    return response_string
