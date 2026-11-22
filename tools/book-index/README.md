# book-index

`book-index` is a small standalone Go command-line tool that reads a JSON array of book records from standard input, removes duplicates, normalizes whitespace, and writes a JSON array to standard output.

## Behavior

- Input: a JSON array of objects
- Required fields used for deduplication: `title` and `author`-style fields
- Whitespace normalization: trims leading/trailing whitespace and collapses internal whitespace runs to a single space
- Duplicate detection: case-insensitive `title + author` key
- Output order: first occurrence of each unique book is preserved
- Output: valid JSON array on stdout

## Usage

```bash
cat books.json | go run ./tools/book-index > unique-books.json
```

The tool reads from stdin and prints to stdout, so it can be used in pipelines.

## Input example

```json
[
  {"title": "  The Hobbit ", "author": "J.R.R. Tolkien"},
  {"title": "the hobbit", "author": "j.r.r. tolkien"},
  {"title": "Dune", "author": "Frank Herbert"}
]
```

## Output example

```json
[
  {
    "author": "J.R.R. Tolkien",
    "title": "The Hobbit"
  },
  {
    "author": "Frank Herbert",
    "title": "Dune"
  }
]
```

## Notes

- The tool uses only the Go standard library.
- Invalid JSON or missing required fields cause a non-zero exit status.
