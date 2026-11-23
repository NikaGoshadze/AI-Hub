# book-report

A small command-line tool that reads a JSON array of books from standard input and writes a JSON object mapping author names to book counts.

Each book object must contain an `author` field.

## Build

From the `tools/book-report` directory:

```sh
go build
```

## Test

From the `tools/book-report` directory:

```sh
go test
```

## Run

From the `tools/book-report` directory:

```sh
go run . < input.json
```

Example input:

```json
[{"author":"Ada"},{"author":"Bob"},{"author":"Ada"}]
```

Example output:

```json
{"Ada":2,"Bob":1}
```
