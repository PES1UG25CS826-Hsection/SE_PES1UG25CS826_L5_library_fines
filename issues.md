# Static Analysis Issues

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Use of `eval()` (Bandit B307, Pylint W0123) | Security (Medium) | 45 | `fine_from_rule` passes text to `eval`, so a crafted rule can run arbitrary code | Replaced with an `ast`-based evaluator allowing only numbers, `days`, `+`, `-`, `*` |
| Bare `except: pass` (Bandit B110, Pylint W0702, Flake8 E722) | Security / Bug (Low) | 21-22 | Swallows every error silently | Catch `KeyError` and `ValueError` only and print a message |
| Mutable default argument (Pylint W0102) | Bug | 9 | `dates=[]` is shared across calls, so the loan-date count keeps growing | Default to `None` and create the list inside the function |
| Renewal changes global fine rate (Pylint W0603) | Bug (logic) | 27-30 | Renewing for more than 14 days raised `FINE_PER_DAY` for everyone, so 5 days cost 15 instead of 10 | Removed the global mutation |
| Files not closed safely, no encoding (Pylint R1732, W1514) | Quality | 34, 40 | `open()` without `with` can leak handles | Used `with open(..., encoding="utf-8")` |
| Unused import `os` (Pylint W0611, Flake8 F401) | Quality | 2 | Dead import | Removed |
| Function name `renewBook` (Pylint C0103) | Style | 27 | Not snake_case | Renamed to `renew_book` |
| Missing docstrings (Pylint C0114, C0116) | Style | 1, 9, 16, 24, 27, 33, 39, 44, 47, 52 | No documentation | Added docstrings |
| `%` string formatting (Pylint C0209) | Style | 14 | f-string is clearer | Switched to f-strings |
| Blank lines and line length (Flake8 E302, E305, E501) | Style | 9-68, 14, 31 | Missing blank lines; lines over 79 characters | Added blank lines and wrapped long lines |
| Negative fine, non-string book ID, silent empty ID (found by running the program) | Bug (logic) | 9-12, 24-25 | `calculate_fine(-3)` gave -9; `4521` accepted as a book ID | Negative days give 0; invalid IDs rejected with a message |

**Results:** Pylint 6.07/10 to X.XX/10 (put your real score). Bandit 2 issues to 0. Flake8 14 issues to 0.
