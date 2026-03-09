# Project 10 – Jack Syntax Analyzer
**Author:** Taleh Malikov
**Course:** Nand2Tetris / Computer Systems

---

## Overview

This project implements the front-end of the Jack compiler as described in
*The Elements of Computing Systems* (Nand2Tetris), Chapter 10.

It produces two XML outputs per `.jack` source file:

| Output file | Contents |
|---|---|
| `XxxT.xml` | Flat token stream from the **tokenizer** |
| `Xxx.xml`  | Structured parse tree from the **parser** |

---

## Files

| File | Role |
|---|---|
| `JackAnalyzer.py`     | Entry point – handles file/dir I/O |
| `JackTokenizer.py`    | Lexical analysis (regex-based tokenizer) |
| `CompilationEngine.py`| Recursive-descent parser → XML |

---

## Requirements

- Python 3.10 or later (uses `str | None` union type hint syntax)
- No third-party libraries required

---

## How to Run

### Single file
```bash
python JackAnalyzer.py path/to/Xxx.jack
```
Produces `XxxT.xml` and `Xxx.xml` in the **same directory** as the source file.

### Entire directory
```bash
python JackAnalyzer.py path/to/SquareDance/
python JackAnalyzer.py path/to/ArrayTest/
```
Processes every `.jack` file found in that directory.

---

## Testing

Use the supplied **TextComparer** utility to diff your output against the
reference files. Since your output files have the same names as the compare
files, keep them in **separate directories**, e.g.:

```
SquareDance/
    Square.jack  Main.jack  SquareGame.jack     ← source
    Square.xml   Main.xml   SquareGame.xml      ← generated (parser)
    SquareT.xml  MainT.xml  SquareGameT.xml     ← generated (tokenizer)

SquareDance_compare/
    Square.xml   Main.xml   SquareGame.xml      ← reference parser output
    SquareT.xml  MainT.xml  SquareGameT.xml     ← reference tokenizer output
```

Then compare:
```bash
TextComparer SquareDance/Main.xml      SquareDance_compare/Main.xml
TextComparer SquareDance/MainT.xml     SquareDance_compare/MainT.xml
```

---

## Design Notes

### Tokenizer (`JackTokenizer.py`)
- A single compiled regular expression handles all token types plus comments
  in one pass over the source text.
- Comments (`//` and `/* … */`) are consumed by the regex and silently dropped.
- XML special characters (`<`, `>`, `&`, `"`) are escaped in all output.

### Parser (`CompilationEngine.py`)
- Pure recursive-descent, one method per grammar rule.
- One-token look-ahead via `JackTokenizer.peek()` is used only in `compileTerm`
  to distinguish plain varName / array access / subroutine call.
- `SyntaxError` is raised with a descriptive message on unexpected tokens.

### XML escaping
| Jack source | XML output |
|---|---|
| `<`  | `&lt;`  |
| `>`  | `&gt;`  |
| `&`  | `&amp;` |
| `"`  | `&quot;`|
