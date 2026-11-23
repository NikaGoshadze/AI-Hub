from flask import Flask, render_template, request, session

from books_app.main import search_book_database

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = app.config.get("SECRET_KEY", "dev-secret-key")


def _load_favorites():
    favorites = session.get("favorites", [])
    if not isinstance(favorites, list):
        return []
    normalized = []
    seen = set()
    for item in favorites:
        if not isinstance(item, dict):
            continue
        title = str(item.get("title", "")).strip()
        authors = str(item.get("authors", "")).strip()
        key = (title, authors)
        if not title or key in seen:
            continue
        seen.add(key)
        normalized.append({"title": title, "authors": authors})
    if normalized != favorites:
        session["favorites"] = normalized
    return normalized


def _save_favorite(favorites, title, authors):
    key = (title, authors)
    if any((fav.get("title"), fav.get("authors")) == key for fav in favorites):
        return favorites
    favorites = favorites + [{"title": title, "authors": authors}]
    session["favorites"] = favorites
    return favorites


def _remove_favorite(favorites, title, authors):
    favorites = [fav for fav in favorites if (fav.get("title"), fav.get("authors")) != (title, authors)]
    session["favorites"] = favorites
    return favorites


@app.route("/", methods=["GET", "POST"])
def index():
    query = ""
    results = ""
    favorites = _load_favorites()
    search_items = []

    if request.method == "POST":
        action = request.form.get("action", "search")
        if action == "search":
            query = request.form.get("query", "").strip()
            if query:
                results = search_book_database(query)
                search_items = [
                    line.removeprefix("- Title: ")
                    for line in results.splitlines()
                    if line.startswith("- Title: ")
                ]
        elif action in {"save", "remove"}:
            query = request.form.get("query", "").strip()
            results = request.form.get("results", "")
            title = request.form.get("title", "").strip()
            authors = request.form.get("authors", "").strip()
            if action == "save" and title:
                favorites = _save_favorite(favorites, title, authors)
            elif action == "remove" and title:
                favorites = _remove_favorite(favorites, title, authors)
            search_items = [
                line.removeprefix("- Title: ")
                for line in results.splitlines()
                if line.startswith("- Title: ")
            ]

    return render_template(
        "index.html",
        query=query,
        results=results,
        favorites=favorites,
        search_items=search_items,
    )


if __name__ == "__main__":
    app.run(debug=True)