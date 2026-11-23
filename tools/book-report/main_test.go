package main

import (
	"bytes"
	"strings"
	"testing"
)

func TestRunCountsAuthors(t *testing.T) {
	in := strings.NewReader(`[{"author":"Ada"},{"author":"Bob"},{"author":"Ada"}]`)
	var out bytes.Buffer
	var errOut bytes.Buffer

	if err := run(in, &out, &errOut); err != nil {
		t.Fatalf("run returned error: %v", err)
	}

	got := out.String()
	if got != "{\"Ada\":2,\"Bob\":1}\n" && got != "{\"Bob\":1,\"Ada\":2}\n" {
		t.Fatalf("unexpected output: %q", got)
	}
}

func TestRunRejectsInvalidJSON(t *testing.T) {
	in := strings.NewReader(`not json`)
	var out bytes.Buffer
	var errOut bytes.Buffer

	if err := run(in, &out, &errOut); err == nil {
		t.Fatal("expected error for invalid JSON")
	}
}
