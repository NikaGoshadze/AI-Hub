# Word Count Examples

Each example reads exactly one line from standard input, counts whitespace-separated words, and prints a single integer.
An empty input line prints `0`.

## Java

Build:

```bash
javac WordCount.java
```

Run:

```bash
printf 'hello world\n' | java WordCount
```

## Rust

Build:

```bash
rustc word_count.rs -o word_count
```

Run:

```bash
printf 'hello world\n' | ./word_count
```

## C++

Build:

```bash
c++ -std=c++17 -O2 -o word_count word_count.cpp
```

Run:

```bash
printf 'hello world\n' | ./word_count
```
