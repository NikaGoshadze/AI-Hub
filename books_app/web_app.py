from flask import Flask, render_template, request

from books_app.main import search_book_database

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route("/", methods=["GET", "POST"])
def index():
    query = ""
    results = ""
    if request.method == "POST":
        query = request.form.get("query", "").strip()
        if query:
            results = search_book_database(query)
    return render_template("index.html", query=query, results=results)


if __name__ == "__main__":
    app.run(debug=True)