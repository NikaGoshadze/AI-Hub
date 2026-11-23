from flask import Flask, render_template, request

from books_app.main import search_book_database

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route("/", methods=["GET", "POST"])
def index():
    query = ""
    results = ""
    if request.method == "POST":
        query = request.form.get("query", "").strip()
        if not query:
            results = "Please enter a search term to look for matching books."
        else:
            try:
                results = search_book_database(query)
            except Exception:
                results = (
                    "Sorry, the book search service is temporarily unavailable. "
                    "Please try again in a moment."
                )
    return render_template("index.html", query=query, results=results)


if __name__ == "__main__":
    app.run(debug=True)