from flask import Flask, jsonify, render_template, request

from books_app.main import search_book_database

app = Flask(__name__, template_folder="templates", static_folder="static")


def _format_results(raw_results):
    if not raw_results:
        return []

    formatted = []
    for item in raw_results:
        title = None
        authors = None

        if isinstance(item, dict):
            title = item.get("title")
            authors = item.get("authors")
        else:
            title = getattr(item, "title", None)
            authors = getattr(item, "authors", None)

        if isinstance(authors, tuple):
            authors = list(authors)

        formatted.append({
            "title": title,
            "authors": authors,
        })
    return formatted


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html", query="")


@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query", "").strip()
    if not query:
        return jsonify({"results": [], "count": 0, "error": "Please enter a search query."}), 400

    try:
        raw_results = search_book_database(query)
        results = _format_results(raw_results)
        return jsonify({"results": results, "count": len(results)})
    except Exception:
        return jsonify({"results": [], "count": 0, "error": "Sorry, something went wrong while searching for books."}), 500


if __name__ == "__main__":
    app.run(debug=True)