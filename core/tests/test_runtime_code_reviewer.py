import pytest
import os
from core.runtime.runtime_code_reviewer import RuntimeCodeReviewer, CodeReview, ReviewComment


@pytest.fixture
def reviewer():
    return RuntimeCodeReviewer()


GOOD_CODE = '''"""Module for doing useful things."""


def calculate_sum(a, b):
    """Return the sum of a and b."""
    try:
        return a + b
    except TypeError as e:
        raise ValueError(f"Invalid inputs: {e}")


if __name__ == "__main__":
    print(calculate_sum(1, 2))
'''

BAD_CODE = "def BadFunction():\n    eval('dangerous')\n    pass\n"

EMPTY_CODE = ""

SYNTAX_ERROR_CODE = "def broken(\n    pass"


def test_review_good_code(reviewer):
    review = reviewer.review_code(GOOD_CODE)
    assert isinstance(review, CodeReview)
    assert review.score >= 70


def test_review_empty_code(reviewer):
    review = reviewer.review_code(EMPTY_CODE)
    assert review.passed is False
    assert review.score == 0


def test_review_syntax_error(reviewer):
    review = reviewer.review_code(SYNTAX_ERROR_CODE)
    assert review.passed is False
    assert any(c.severity == "error" for c in review.comments)


def test_review_detects_eval(reviewer):
    review = reviewer.review_code(BAD_CODE)
    assert any("eval" in c.message for c in review.comments)


def test_review_detects_bad_naming(reviewer):
    code = "def BadFunctionName():\n    pass\n"
    review = reviewer.review_code(code)
    assert any("snake_case" in c.message for c in review.comments)


def test_review_score_penalized_for_issues(reviewer):
    review = reviewer.review_code(BAD_CODE)
    assert review.score < 100


def test_review_file_missing(reviewer, tmp_path):
    review = reviewer.review_file("/nonexistent/path.py")
    assert review.passed is False


def test_review_file_valid(reviewer, tmp_path):
    f = tmp_path / "test.py"
    f.write_text(GOOD_CODE)
    review = reviewer.review_file(str(f))
    assert review.score >= 70


def test_review_to_dict(reviewer):
    review = reviewer.review_code(GOOD_CODE)
    d = review.to_dict()
    assert "score" in d
    assert "passed" in d
    assert "comments" in d
    assert "errors" in d


def test_review_summary(reviewer):
    review = reviewer.review_code(GOOD_CODE)
    summary = review.summary()
    assert "Score" in summary


def test_history_recorded(reviewer):
    reviewer.review_code(GOOD_CODE)
    reviewer.review_code(BAD_CODE)
    assert len(reviewer.get_history()) == 2


def test_aggregate_score(reviewer):
    r1 = reviewer.review_code(GOOD_CODE)
    r2 = reviewer.review_code(GOOD_CODE)
    score = reviewer.get_aggregate_score([r1, r2])
    assert isinstance(score, int)
    assert 0 <= score <= 100


def test_review_comment_to_dict():
    c = ReviewComment("warning", "style", "Use snake_case", 10)
    d = c.to_dict()
    assert d["severity"] == "warning"
    assert d["line"] == 10


def test_review_comment_str():
    c = ReviewComment("error", "syntax", "Broken code", 5)
    s = str(c)
    assert "ERROR" in s
    assert "line 5" in s


def test_class_naming_detected(reviewer):
    code = "class bad_class_name:\n    def method(self):\n        pass\n"
    review = reviewer.review_code(code)
    assert any("PascalCase" in c.message for c in review.comments)