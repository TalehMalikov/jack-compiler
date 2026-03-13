# Jack Compiler - Projects 10 & 11
**Author:** Taleh Malikov  
**Repo:** https://github.com/TalehMalikov/jack-compiler

---

## Overview

This project implements a full Jack compiler in two stages:

- **Project 10** — Syntax analysis: tokenizer and recursive-descent parser, produces XML output
- **Project 11** — Code generation: compiles Jack source to Hack VM code

---

## Files
```
malikovTalehProject11/
├── src/
│   ├── JackAnalyzer.py       - Project 10 entry point (produces XML)
│   ├── JackCompiler.py       - Project 11 entry point (produces VM code)
│   ├── JackTokenizer.py      - tokenizer (shared by both projects)
│   ├── CompilationEngine.py  - Project 11 compiler (produces VM code)
│   ├── SymbolTable.py        - manages class and subroutine symbol tables
│   └── VMWriter.py           - writes VM commands to output
├── tests_project_10/
│   ├── Square/
│   ├── Square_compare/
│   ├── ArrayTest/
│   ├── ArrayTest_compare/
│   ├── ExpressionLessSquare/
│   └── ExpressionLessSquare_compare/
├── tests_project_11/
│   ├── Seven/
│   ├── ConvertToBin/
│   ├── Square/
│   ├── Average/
│   ├── Pong/
│   └── ComplexArrays/
└── README.md
```

---

## Requirements

- Python 3.6 or later
- No third-party libraries needed

---

## Project 10 - Syntax Analyzer

### How to Run
```
python src/JackAnalyzer.py path/to/Xxx.jack
python src/JackAnalyzer.py path/to/directory/
```

Produces `XxxT.xml` (token stream) and `Xxx.xml` (parse tree) alongside the source files.

### How to Test

**Important:** never put `.jack` files and reference `.xml` compare files in the same folder.
```
python src/JackAnalyzer.py tests_project_10/Square
python src/JackAnalyzer.py tests_project_10/ArrayTest
python src/JackAnalyzer.py tests_project_10/ExpressionLessSquare
```

Then compare with TextComparer (Windows):
```
cmd /c "<path-to-nand2tetris>\tools\TextComparer.bat" tests_project_10/Square/Main.xml tests_project_10/Square_compare/Main.xml
cmd /c "<path-to-nand2tetris>\tools\TextComparer.bat" tests_project_10/Square/MainT.xml tests_project_10/Square_compare/MainT.xml
cmd /c "<path-to-nand2tetris>\tools\TextComparer.bat" tests_project_10/Square/Square.xml tests_project_10/Square_compare/Square.xml
cmd /c "<path-to-nand2tetris>\tools\TextComparer.bat" tests_project_10/Square/SquareT.xml tests_project_10/Square_compare/SquareT.xml
cmd /c "<path-to-nand2tetris>\tools\TextComparer.bat" tests_project_10/Square/SquareGame.xml tests_project_10/Square_compare/SquareGame.xml
cmd /c "<path-to-nand2tetris>\tools\TextComparer.bat" tests_project_10/Square/SquareGameT.xml tests_project_10/Square_compare/SquareGameT.xml
cmd /c "<path-to-nand2tetris>\tools\TextComparer.bat" tests_project_10/ArrayTest/Main.xml tests_project_10/ArrayTest_compare/Main.xml
cmd /c "<path-to-nand2tetris>\tools\TextComparer.bat" tests_project_10/ArrayTest/MainT.xml tests_project_10/ArrayTest_compare/MainT.xml
cmd /c "<path-to-nand2tetris>\tools\TextComparer.bat" tests_project_10/ExpressionLessSquare/Main.xml tests_project_10/ExpressionLessSquare_compare/Main.xml
cmd /c "<path-to-nand2tetris>\tools\TextComparer.bat" tests_project_10/ExpressionLessSquare/MainT.xml tests_project_10/ExpressionLessSquare_compare/MainT.xml
cmd /c "<path-to-nand2tetris>\tools\TextComparer.bat" tests_project_10/ExpressionLessSquare/Square.xml tests_project_10/ExpressionLessSquare_compare/Square.xml
cmd /c "<path-to-nand2tetris>\tools\TextComparer.bat" tests_project_10/ExpressionLessSquare/SquareT.xml tests_project_10/ExpressionLessSquare_compare/SquareT.xml
cmd /c "<path-to-nand2tetris>\tools\TextComparer.bat" tests_project_10/ExpressionLessSquare/SquareGame.xml tests_project_10/ExpressionLessSquare_compare/SquareGame.xml
cmd /c "<path-to-nand2tetris>\tools\TextComparer.bat" tests_project_10/ExpressionLessSquare/SquareGameT.xml tests_project_10/ExpressionLessSquare_compare/SquareGameT.xml
```

All 14 comparisons should end with `Comparison ended successfully`.

---

## Project 11 - Code Generation

### How to Run
```
python src/JackCompiler.py path/to/Xxx.jack
python src/JackCompiler.py path/to/directory/
```

Produces a `Xxx.vm` file alongside each `.jack` source file.

### How to Test

#### Step 1 — Compile the test programs
```
python src/JackCompiler.py tests_project_11/Seven
python src/JackCompiler.py tests_project_11/ConvertToBin
python src/JackCompiler.py tests_project_11/Square
python src/JackCompiler.py tests_project_11/Average
python src/JackCompiler.py tests_project_11/Pong
python src/JackCompiler.py tests_project_11/ComplexArrays
```

#### Step 2 — Run in the VM Emulator

Open `nand2tetris/tools/VMEmulator.bat`, load the compiled folder, and run:

- **Seven** — should print `7` on screen
- **ConvertToBin** — set RAM[8000] to any number, run, check RAM[8001-8016] for binary output
- **Square** — interactive square, move with arrow keys
- **Average** — enter numbers one by one, type `0` to stop, prints the average
- **Pong** — pong game, control bat with arrow keys
- **ComplexArrays** — prints computed array values to screen