from flask import Flask, render_template, request

from books_app.main import lookup_book_database

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route("/", methods=["GET", "POST"])
def index():
    query = ""
    results = None
    result_count = None
    error_message = None
    if request.method == "POST":
        query = request.form.get("query", "").strip()
        if query:
            try:
                results, result_count = lookup_book_database(query)
            except Exception:
                error_message = "Sorry, we couldn’t complete that search right now. Please try again."
            else:
                if result_count == 0:
                    results = []
        return render_template("index.html", query=query, results=results, result_count=result_count, error_message=error_message)
    return render_template("index.html", query=query, results=results, result_count=result_count, error_message=error_message)


if __name__ == "__main__":
    app.run(debug=True)