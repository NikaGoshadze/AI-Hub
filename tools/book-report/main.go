package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"os"
)

type book struct {
	Author string `json:"author"`
}

func run(r io.Reader, w io.Writer, errw io.Writer) error {
	data, err := io.ReadAll(r)
	if err != nil {
		return err
	}

	var books []book
	if err := json.Unmarshal(data, &books); err != nil {
		return err
	}

	counts := make(map[string]int)
	for _, b := range books {
		counts[b.Author]++
	}

	enc := json.NewEncoder(w)
	if err := enc.Encode(counts); err != nil {
		return err
	}
	return nil
}

func main() {
	if err := run(os.Stdin, os.Stdout, os.Stderr); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}

var _ = errors.New
