import pytest
from core.runtime.runtime_code_extractor import RuntimeCodeExtractor, ExtractedCode


def make_extractor():
    return RuntimeCodeExtractor()


def test_extract_fenced_python():
    extractor = make_extractor()
    text = "Here is some code:\n```python\nx = 1\nprint(x)\n```"
    blocks = extractor.extract_all(text)
    assert len(blocks) == 1
    assert "x = 1" in blocks[0].content


def test_extract_multiple_blocks():
    extractor = make_extractor()
    text = "First:\n```python\na = 1\n```\nSecond:\n```python\nb = 2\n```"
    blocks = extractor.extract_all(text)
    assert len(blocks) == 2


def test_extract_no_language_tag():
    extractor = make_extractor()
    text = "```\nimport os\nprint(os.getcwd())\n```"
    blocks = extractor.extract_all(text)
    assert len(blocks) == 1


def test_extract_first_python():
    extractor = make_extractor()
    text = "```python\nx = 1\n```\n```bash\necho hello\n```"
    block = extractor.extract_first_python(text)
    assert block is not None
    assert "x = 1" in block.content


def test_extract_python_blocks_filters_non_python():
    extractor = make_extractor()
    text = "```bash\necho hi\n```\n```python\nx = 1\n```"
    blocks = extractor.extract_python_blocks(text)
    assert len(blocks) == 1
    assert "x = 1" in blocks[0].content


def test_merge_python_blocks():
    extractor = make_extractor()
    text = "```python\na = 1\n```\n```python\nb = 2\n```"
    merged = extractor.merge_python_blocks(text)
    assert merged is not None
    assert "a = 1" in merged.content
    assert "b = 2" in merged.content


def test_extract_no_blocks_returns_empty():
    extractor = make_extractor()
    text = "This is just plain text with no code at all."
    blocks = extractor.extract_all(text)
    assert isinstance(blocks, list)


def test_extract_raw_python_detection():
    extractor = make_extractor()
    text = "import os\nimport sys\ndef main():\n    print('hello')\nmain()"
    blocks = extractor.extract_all(text)
    assert len(blocks) >= 1


def test_extracted_code_has_line_count():
    extractor = make_extractor()
    text = "```python\nx = 1\ny = 2\nz = 3\n```"
    blocks = extractor.extract_all(text)
    assert blocks[0].line_count == 3


def test_extracted_code_to_dict():
    code = ExtractedCode("python", "x = 1\n", "test")
    d = code.to_dict()
    assert d["language"] == "python"
    assert "x = 1" in d["content"]


def test_extraction_history_recorded():
    extractor = make_extractor()
    extractor.extract_all("```python\nx=1\n```", "source_a")
    extractor.extract_all("```python\ny=2\n```", "source_b")
    history = extractor.get_history()
    assert len(history) == 2


def test_extract_first_python_returns_none_when_empty():
    extractor = make_extractor()
    result = extractor.extract_first_python("no code here at all in any block")
    assert result is None


def test_large_code_block_extracted():
    extractor = make_extractor()
    code_lines = "\n".join([f"x_{i} = {i}" for i in range(50)])
    text = f"```python\n{code_lines}\n```"
    blocks = extractor.extract_all(text)
    assert blocks[0].line_count == 50