# Project 10 - Jack Syntax Analyzer
**Author:** Taleh Malikov
**Repo:** https://github.com/TalehMalikov/jack-compiler

---

## Overview

This project implements the front-end of the Jack compiler (syntax analysis).
It takes `.jack` source files as input and produces two XML output files per class:

- `XxxT.xml` — flat token stream from the tokenizer
- `Xxx.xml`  — structured parse tree from the parser

---

## Files

```
malikovTalehProject10/
├── src/
│   ├── JackAnalyzer.py       - entry point, handles file/directory input
│   ├── JackTokenizer.py      - tokenizer (breaks source into tokens)
│   └── CompilationEngine.py  - recursive-descent parser (produces XML)
├── tests/
│   ├── Square/               - Square test .jack files
│   ├── Square_compare/       - Square reference XML files
│   ├── ArrayTest/            - ArrayTest .jack files
│   ├── ArrayTest_compare/    - ArrayTest reference XML files
│   ├── ExpressionLessSquare/ - ExpressionLessSquare .jack files
│   └── ExpressionLessSquare_compare/ - ExpressionLessSquare reference XML files
└── README.md
```

---

## Requirements

- Python 3.6 or later
- No third-party libraries needed

---

## How to Run

### Single file
```
python src/JackAnalyzer.py path/to/Xxx.jack
```

### Entire directory
```
python src/JackAnalyzer.py path/to/directory/
```

This will generate `XxxT.xml` (tokenizer output) and `Xxx.xml` (parser output)
in the same folder as the source `.jack` files.

---

## How to Test

**Important:** never put your `.jack` files and the reference `.xml` compare files
in the same folder, otherwise running the analyzer will overwrite them.
Keep them in separate directories as shown in the file structure above.

### Step 1 — Run the analyzer on each test directory

```
python src/JackAnalyzer.py tests/Square
python src/JackAnalyzer.py tests/ArrayTest
python src/JackAnalyzer.py tests/ExpressionLessSquare
```

### Step 2 — Compare output against reference files using TextComparer

Replace `<path-to-nand2tetris>` with your local Nand2Tetris installation path.

**On Windows:**
```
cmd /c "<path-to-nand2tetris>\tools\TextComparer.bat" tests/Square/Main.xml tests/Square_compare/Main.xml
cmd /c "<path-to-nand2tetris>\tools\TextComparer.bat" tests/Square/MainT.xml tests/Square_compare/MainT.xml
cmd /c "<path-to-nand2tetris>\tools\TextComparer.bat" tests/Square/Square.xml tests/Square_compare/Square.xml
cmd /c "<path-to-nand2tetris>\tools\TextComparer.bat" tests/Square/SquareT.xml tests/Square_compare/SquareT.xml
cmd /c "<path-to-nand2tetris>\tools\TextComparer.bat" tests/Square/SquareGame.xml tests/Square_compare/SquareGame.xml
cmd /c "<path-to-nand2tetris>\tools\TextComparer.bat" tests/Square/SquareGameT.xml tests/Square_compare/SquareGameT.xml

cmd /c "<path-to-nand2tetris>\tools\TextComparer.bat" tests/ArrayTest/Main.xml tests/ArrayTest_compare/Main.xml
cmd /c "<path-to-nand2tetris>\tools\TextComparer.bat" tests/ArrayTest/MainT.xml tests/ArrayTest_compare/MainT.xml

cmd /c "<path-to-nand2tetris>\tools\TextComparer.bat" tests/ExpressionLessSquare/Main.xml tests/ExpressionLessSquare_compare/Main.xml
cmd /c "<path-to-nand2tetris>\tools\TextComparer.bat" tests/ExpressionLessSquare/MainT.xml tests/ExpressionLessSquare_compare/MainT.xml
cmd /c "<path-to-nand2tetris>\tools\TextComparer.bat" tests/ExpressionLessSquare/Square.xml tests/ExpressionLessSquare_compare/Square.xml
cmd /c "<path-to-nand2tetris>\tools\TextComparer.bat" tests/ExpressionLessSquare/SquareT.xml tests/ExpressionLessSquare_compare/SquareT.xml
cmd /c "<path-to-nand2tetris>\tools\TextComparer.bat" tests/ExpressionLessSquare/SquareGame.xml tests/ExpressionLessSquare_compare/SquareGame.xml
cmd /c "<path-to-nand2tetris>\tools\TextComparer.bat" tests/ExpressionLessSquare/SquareGameT.xml tests/ExpressionLessSquare_compare/SquareGameT.xml
```

**On Mac/Linux:**
```
<path-to-nand2tetris>/tools/TextComparer.sh tests/Square/Main.xml tests/Square_compare/Main.xml
```
(repeat for each file as above)

### Step 3 — Check results

- `Comparison ended successfully` — the file is correct ✓
- `Comparison failed in line X`   — there is a mismatch at that line ✗

All 14 comparisons should end successfully.

