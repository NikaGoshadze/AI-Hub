package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"strings"
)

type bookRecord struct {
	Title  string `json:"title"`
	Author string `json:"author,omitempty"`
	Authors string `json:"authors,omitempty"`

	TitleText  string `json:"title_text,omitempty"`
	AuthorText string `json:"author_text,omitempty"`
}

func main() {
	if err := run(os.Stdin, os.Stdout, os.Stderr); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}

func run(stdin io.Reader, stdout io.Writer, stderr io.Writer) error {
	var raw []map[string]json.RawMessage
	dec := json.NewDecoder(stdin)
	dec.DisallowUnknownFields()
	if err := dec.Decode(&raw); err != nil {
		return fmt.Errorf("decode input: %w", err)
	}
	if dec.More() {
		return fmt.Errorf("decode input: extra data after JSON array")
	}

	seen := make(map[string]struct{}, len(raw))
	out := make([]map[string]any, 0, len(raw))

	for _, item := range raw {
		title, titleOut, err := normalizedField(item, []string{"title", "title_text"})
		if err != nil {
			return err
		}
		author, authorOut, err := normalizedField(item, []string{"author", "authors", "author_text"})
		if err != nil {
			return err
		}

		key := strings.ToLower(title) + "\x00" + strings.ToLower(author)
		if _, ok := seen[key]; ok {
			continue
		}
		seen[key] = struct{}{}

		cleaned := make(map[string]any, len(item))
		for k, v := range item {
			cleaned[k] = jsonValue(v)
		}
		cleaned["title"] = titleOut
		if authorOut != "" {
			cleaned["author"] = authorOut
			delete(cleaned, "authors")
			delete(cleaned, "author_text")
		} else {
			delete(cleaned, "author")
			delete(cleaned, "authors")
			delete(cleaned, "author_text")
		}
		delete(cleaned, "title_text")
		cleaned["title"] = titleOut
		out = append(out, cleaned)
	}

	enc := json.NewEncoder(stdout)
	enc.SetIndent("", "  ")
	return enc.Encode(out)
}

func normalizedField(item map[string]json.RawMessage, keys []string) (key string, out string, err error) {
	for _, k := range keys {
		if raw, ok := item[k]; ok {
			var s string
			if err := json.Unmarshal(raw, &s); err != nil {
				return "", "", fmt.Errorf("field %q must be a string", k)
			}
			n := normalizeWhitespace(s)
			return n, n, nil
		}
	}
	return "", "", fmt.Errorf("missing required field in %v", keys)
}

func normalizeWhitespace(s string) string {
	return strings.Join(strings.Fields(strings.TrimSpace(s)), " ")
}

func jsonValue(raw json.RawMessage) any {
	var v any
	_ = json.Unmarshal(raw, &v)
	return v
}
