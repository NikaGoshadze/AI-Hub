package main

import (
	"bytes"
	"encoding/json"
	"strings"
	"testing"
)

func TestRunNormalizesDeduplicatesAndPreservesOrder(t *testing.T) {
	input := `[
	  {"title":"  The   Hobbit  ","author":"J.R.R.   Tolkien","year":1937},
	  {"title":"the hobbit","author":"j.r.r. tolkien","year":9999},
	  {"title":"Dune","author":" Frank   Herbert ","year":1965}
	]`

	var stdout bytes.Buffer
	if err := run(strings.NewReader(input), &stdout, &bytes.Buffer{}); err != nil {
		t.Fatalf("run() returned error: %v", err)
	}

	var got []map[string]any
	if err := json.Unmarshal(stdout.Bytes(), &got); err != nil {
		t.Fatalf("output is not valid JSON: %v", err)
	}

	if len(got) != 2 {
		t.Fatalf("expected 2 unique records, got %d", len(got))
	}
	if got[0]["title"] != "The Hobbit" || got[0]["author"] != "J.R.R. Tolkien" {
		t.Fatalf("first record not normalized as expected: %#v", got[0])
	}
	if got[1]["title"] != "Dune" || got[1]["author"] != "Frank Herbert" {
		t.Fatalf("second record not preserved as expected: %#v", got[1])
	}
}
