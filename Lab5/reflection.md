# Lab 5 — Reflection

### 1. What is static code analysis?

Static code analysis examines source code without executing the program. It helps identify potential bugs, security vulnerabilities, and coding-style problems.

### 2. What are the purposes of Pylint, Bandit, and Flake8?

Pylint checks code quality and programming practices. Bandit identifies potentially insecure Python coding patterns. Flake8 checks style and formatting issues.

### 3. What issues did you fix?

I fixed unsafe temporary-file handling, replaced an assertion used for runtime validation, corrected a mutable default argument, and replaced a bare exception handler with specific exception handling. I also improved documentation, naming, file handling, and formatting.

### 4. What did you learn?

I learned that static analysis tools identify different types of problems in the same program. Fixing the underlying issues improves code quality, readability, and security. Rerunning the tools verifies whether the changes addressed the reported findings. Runtime testing also helps identify errors that static analysis may not catch.