import ast
import re
from datetime import datetime


class ReviewComment:

    def __init__(self, severity, category, message, line=None):
        self.severity = severity  # "error", "warning", "suggestion", "info"
        self.category = category
        self.message = message
        self.line = line

    def to_dict(self):
        return {
            "severity": self.severity,
            "category": self.category,
            "message": self.message,
            "line": self.line,
        }

    def __str__(self):
        loc = f" (line {self.line})" if self.line else ""
        return f"[{self.severity.upper()}] {self.category}: {self.message}{loc}"


class CodeReview:

    def __init__(self, file_path, comments, score, passed):
        self.file_path = file_path
        self.comments = comments
        self.score = score
        self.passed = passed
        self.reviewed_at = datetime.now().isoformat()

    def to_dict(self):
        return {
            "file_path": self.file_path,
            "comments": [c.to_dict() for c in self.comments],
            "score": self.score,
            "passed": self.passed,
            "reviewed_at": self.reviewed_at,
            "errors": sum(1 for c in self.comments if c.severity == "error"),
            "warnings": sum(1 for c in self.comments if c.severity == "warning"),
            "suggestions": sum(1 for c in self.comments if c.severity == "suggestion"),
        }

    def summary(self):
        d = self.to_dict()
        return (
            f"Score: {self.score}/100 | "
            f"errors={d['errors']} warnings={d['warnings']} suggestions={d['suggestions']}"
        )


class RuntimeCodeReviewer:
    """
    Reviews generated Python code for quality issues.
    - Syntax validation
    - Style checks (function length, naming, complexity)
    - Security flags (exec, eval, __import__)
    - Documentation completeness
    - Common bug patterns
    - Produces scored review with actionable comments
    """

    DANGEROUS_PATTERNS = [
        (r"\beval\s*\(", "eval() usage is dangerous — prefer ast.literal_eval"),
        (r"\bexec\s*\(", "exec() usage can execute arbitrary code"),
        (r"__import__\s*\(", "__import__() is unsafe — use standard imports"),
        (r"os\.system\s*\(", "os.system() is unsafe — use subprocess"),
        (r"pickle\.loads?\s*\(", "pickle.load() can execute arbitrary code"),
        (r"subprocess\.call\s*\(.*shell\s*=\s*True", "shell=True in subprocess is a security risk"),
    ]

    def __init__(self):
        self.review_history = []

    def review_code(self, source, file_path="<code>"):
        comments = []
        score = 100

        if not source or not source.strip():
            return CodeReview(file_path, [
                ReviewComment("error", "content", "Empty file")
            ], 0, False)

        # Syntax check
        try:
            tree = ast.parse(source)
        except SyntaxError as e:
            return CodeReview(file_path, [
                ReviewComment("error", "syntax", f"Syntax error: {e}")
            ], 0, False)

        lines = source.splitlines()

        # Check docstrings
        has_module_docstring = (
            isinstance(tree.body[0], ast.Expr) and
            isinstance(tree.body[0].value, ast.Constant)
        ) if tree.body else False

        if not has_module_docstring:
            comments.append(ReviewComment("suggestion", "documentation", "Add a module-level docstring"))
            score -= 5

        # Check functions/classes
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Function length
                func_lines = node.end_lineno - node.lineno if hasattr(node, "end_lineno") else 0
                if func_lines > 50:
                    comments.append(ReviewComment(
                        "warning", "complexity",
                        f"Function '{node.name}' is {func_lines} lines — consider splitting",
                        node.lineno
                    ))
                    score -= 5

                # Missing docstring
                has_doc = (
                    node.body and
                    isinstance(node.body[0], ast.Expr) and
                    isinstance(node.body[0].value, ast.Constant)
                )
                if not has_doc and not node.name.startswith("_"):
                    comments.append(ReviewComment(
                        "suggestion", "documentation",
                        f"Function '{node.name}' missing docstring",
                        node.lineno
                    ))
                    score -= 2

                # Naming convention
                if not re.match(r"^[a-z_][a-z0-9_]*$", node.name) and not node.name.startswith("__"):
                    comments.append(ReviewComment(
                        "warning", "style",
                        f"Function '{node.name}' should use snake_case",
                        node.lineno
                    ))
                    score -= 3

            elif isinstance(node, ast.ClassDef):
                # Class naming
                if not re.match(r"^[A-Z][a-zA-Z0-9]*$", node.name):
                    comments.append(ReviewComment(
                        "warning", "style",
                        f"Class '{node.name}' should use PascalCase",
                        node.lineno
                    ))
                    score -= 3

        # Security patterns
        for pattern, msg in self.DANGEROUS_PATTERNS:
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line):
                    comments.append(ReviewComment("warning", "security", msg, i))
                    score -= 10

        # Error handling
        has_try = "try:" in source
        has_except = "except" in source
        if not has_try and len(lines) > 20:
            comments.append(ReviewComment(
                "suggestion", "robustness",
                "Consider adding error handling (try/except) for production code"
            ))
            score -= 3

        # Very short file
        if len(lines) < 5:
            comments.append(ReviewComment("warning", "content", "File is very short — may be incomplete"))
            score -= 10

        score = max(0, min(100, score))
        passed = score >= 50 and not any(c.severity == "error" for c in comments)
        review = CodeReview(file_path, comments, score, passed)
        self.review_history.append(review.to_dict())
        return review

    def review_file(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                source = f.read()
            return self.review_code(source, file_path)
        except FileNotFoundError:
            return CodeReview(file_path, [
                ReviewComment("error", "file", f"File not found: {file_path}")
            ], 0, False)

    def review_pipeline_run(self, pipeline_run, workspace_base=None):
        import os
        reviews = []
        for file_info in pipeline_run.written_files:
            file_path = file_info.get("file", "")
            if workspace_base:
                full_path = os.path.join(workspace_base, pipeline_run.run_id, file_path)
            else:
                full_path = file_path
            reviews.append(self.review_file(full_path))
        return reviews

    def get_history(self):
        return list(self.review_history)

    def get_aggregate_score(self, reviews):
        if not reviews:
            return 0
        return round(sum(r.score for r in reviews) / len(reviews))