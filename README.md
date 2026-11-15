# Smart Programming Language Lexical and Syntax Analyzer

## Features
- Identifier DFA and numeric constant DFA
- Explicit stack PDA for balanced (), [] and {}
- CFG recursive-descent parser for assignment and if statements
- Token listing, parser trace, state diagrams and test bench

## Run in Antigravity (Windows)
1. Extract ZIP and open this folder in Antigravity.
2. Open integrated terminal.
3. `python -m venv .venv`
4. `.\.venv\Scripts\Activate.ps1`
5. `pip install -r requirements.txt`
6. `streamlit run app.py`

If activation is blocked:
`Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`
Then activate again.

## Automated tests
`python -m unittest discover -s tests -v`

## Teaching language
Identifier: `[A-Za-z_][A-Za-z0-9_]*`
Number: `digit+` or `digit+ '.' digit+`
Assignment: `id = Expr ;`
If: `if (Condition) { Statement+ }`
Expressions: identifiers, numbers, parentheses, +, -, *, /
Conditions: <, >, <=, >=, ==, !=

Educational subset only; it does not implement semantic analysis or execute code.
