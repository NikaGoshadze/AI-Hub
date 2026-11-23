from flask import Flask, render_template, request

from books_app.book_search import get_book_search_results
from books_app.main import search_book_database

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route("/", methods=["GET", "POST"])
def index():
    query = ""
    author = ""
    results = []
    error = ""
    submitted = False

    if request.method == "POST":
        submitted = True
        query = request.form.get("query", "").strip()
        author = request.form.get("author", "").strip()
        if query:
            try:
                results = get_book_search_results(query, search_book_database, author)
            except Exception as exc:
                error = str(exc)

    return render_template(
        "index.html",
        query=query,
        author=author,
        results=results,
        error=error,
        submitted=submitted,
        result_count=len(results),
    )


if __name__ == "__main__":
    app.run(debug=True)
