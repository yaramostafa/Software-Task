# Data Processing Pipeline with Dynamic Expression Parsing

This repository contains a Python implementation for processing and transforming data records based on configurable arithmetic and regex-based equations. It uses a custom Lexer, Parser, and Interpreter to evaluate mathematical and logical expressions dynamically.

---

## Overview

This project processes data records in real-time by:
- Parsing and interpreting equations provided in a configuration file.
- Performing computations or regex-based matching on incoming data.
  example :
  ATTR+50*(ATTR/10)
  Regex(ATTR, "^dog")
- Storing processed results in a SQLite database.

---

## Architecture (calc1.py)

1. **Lexer**: Converts input strings (equations) into tokens.
2. **Parser**: Constructs an Abstract Syntax Tree (AST) from tokens.
3. **Interpreter**: Traverses the AST to evaluate expressions.
4. **FileReader**: Reads new data records incrementally from a file.
5. **DataProcessor**: Processes records using the provided equation.
6. **SQLiteDataSink**: Stores the processed output into a SQLite database.

---
