import re
from datetime import datetime


class ExtractedCode:

    def __init__(self, language, content, source_hint=""):
        self.language = language
        self.content = content
        self.source_hint = source_hint
        self.extracted_at = datetime.now().isoformat()
        self.line_count = len(content.splitlines())

    def to_dict(self):
        return {
            "language": self.language,
            "content": self.content,
            "source_hint": self.source_hint,
            "line_count": self.line_count,
            "extracted_at": self.extracted_at,
        }


class RuntimeCodeExtractor:
    """
    Extracts executable code blocks from LLM responses.
    Handles markdown fences, inline code, and raw code detection.
    Returns structured ExtractedCode objects ready for RuntimeCodeWriter.
    """

    FENCE_PATTERN = re.compile(
        r"```(\w*)\n(.*?)```",
        re.DOTALL
    )

    PYTHON_KEYWORDS = {
        "import", "from", "def", "class", "if", "for", "while",
        "return", "with", "try", "except", "raise", "print",
    }

    def __init__(self):
        self.extraction_history = []

    def extract_all(self, text, source_hint=""):
        """
        Extract all code blocks from text.
        Returns list of ExtractedCode objects.
        """
        blocks = []

        # Extract fenced code blocks first
        for match in self.FENCE_PATTERN.finditer(text):
            lang = match.group(1).strip().lower() or "python"
            code = match.group(2).strip()
            if code:
                blocks.append(ExtractedCode(lang, code, source_hint))

        # If no fenced blocks, try detecting raw Python
        if not blocks:
            raw = self._detect_raw_python(text)
            if raw:
                blocks.append(ExtractedCode("python", raw, source_hint))

        self.extraction_history.append({
            "source_hint": source_hint,
            "blocks_found": len(blocks),
            "extracted_at": datetime.now().isoformat(),
        })

        return blocks

    def extract_first_python(self, text, source_hint=""):
        """
        Extract the first Python code block found.
        Returns ExtractedCode or None.
        """
        all_blocks = self.extract_all(text, source_hint)
        for block in all_blocks:
            if block.language in ("python", "py", ""):
                return block
        # Return first block of any language if no Python found
        return all_blocks[0] if all_blocks else None

    def extract_python_blocks(self, text, source_hint=""):
        """Extract all Python blocks specifically."""
        all_blocks = self.extract_all(text, source_hint)
        return [b for b in all_blocks if b.language in ("python", "py", "")]

    def merge_python_blocks(self, text, source_hint=""):
        """
        Extract and merge all Python blocks into a single code string.
        Useful when LLM splits code across multiple blocks.
        """
        blocks = self.extract_python_blocks(text, source_hint)
        if not blocks:
            return None
        merged = "\n\n".join(b.content for b in blocks)
        return ExtractedCode("python", merged, source_hint)

    def _detect_raw_python(self, text):
        """
        Detect if text contains raw Python code without fences.
        Looks for Python keywords at the start of lines.
        """
        lines = text.strip().splitlines()
        python_line_count = 0
        for line in lines[:20]:  # check first 20 lines
            stripped = line.strip()
            if not stripped:
                continue
            first_word = stripped.split()[0].rstrip("(:")
            if first_word in self.PYTHON_KEYWORDS:
                python_line_count += 1
        # If >30% of sampled lines look like Python, treat as code
        if python_line_count >= 2:
            return text.strip()
        return None

    def get_history(self):
        return list(self.extraction_history)