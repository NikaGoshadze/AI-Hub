from flask import Flask, jsonify, render_template, request

from books_app.book_search import search_books_structured
from books_app.main import get_vectorstore, search_book_database

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    query = request.form.get("query", "").strip()
    author_filter = request.form.get("author_filter", "").strip()
    count_raw = request.form.get("count", "3").strip()

    try:
        count = int(count_raw) if count_raw else 3
    except ValueError:
        return jsonify({"status": "error", "message": "Result count must be a whole number."}), 400

    if count < 1:
        return jsonify({"status": "error", "message": "Result count must be at least 1."}), 400

    if not query:
        return jsonify({"status": "empty", "message": "Enter a search query to find books.", "results": []})

    try:
        vectorstore = get_vectorstore()
        structured_results = search_books_structured(
            query,
            vectorstore,
            author_filter=author_filter,
            count=count,
        )
    except Exception:
        return jsonify(
            {
                "status": "error",
                "message": "The book search service is temporarily unavailable. Please try again later.",
                "results": [],
            }
        ), 503

    if not structured_results:
        return jsonify(
            {
                "status": "empty",
                "message": "No relevant books found in the database.",
                "results": [],
            }
        )

    return jsonify({"status": "success", "results": structured_results})


@app.route("/cli-search", methods=["GET"])
def cli_search():
    query = request.args.get("query", "").strip()
    if not query:
        return jsonify({"results": ""})
    return jsonify({"results": search_book_database(query)})


if __name__ == "__main__":
    app.run(debug=True)
