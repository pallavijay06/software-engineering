# Lab 5 — Static Code Analysis

## Issues Identified and Fixed

| Issue | Tool | Description | Fix Applied |
|---|---|---|---|
| Unsafe temporary-file creation | Bandit | `tempfile.mktemp()` can cause a race condition. | Replaced it with `tempfile.NamedTemporaryFile()`. |
| Use of `assert` | Bandit | Assertions can be disabled when Python runs with optimization. | Replaced the assertion with an explicit condition. |
| Mutable default argument | Pylint | A default list can be shared across function calls. | Changed the default to `None` and initialized a new list. |
| Bare exception handler | Pylint / Flake8 | A bare `except:` catches too many exceptions. | Replaced it with specific exception handling. |
| Missing documentation and formatting issues | Pylint / Flake8 | Missing docstrings and inconsistent formatting reduce readability. | Added documentation and corrected formatting. |
| Invalid asset and inspection interval | Runtime testing | Invalid values could terminate the program with an exception traceback. | Added validation and handled `ValueError` in `main()`. |

## Verification

The original Pylint score was 6.55/10. The improved version previously achieved 9.82/10.

The final Pylint, Bandit, and Flake8 results are saved in their respective after-fix reports.