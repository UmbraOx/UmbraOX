import ast
from typing import Dict


class PatchContractValidator:
    """
    ENFORCES STRUCTURED OUTPUT FROM LLM PATCH ENGINE

    Prevents:
    - markdown injection
    - partial file corruption
    - invalid Python output
    """

    BEGIN = "===BEGIN FILE==="
    END = "===END FILE==="

    # -------------------------
    # PARSE LLM OUTPUT
    # -------------------------
    def extract_code(self, raw: str) -> str:
        if self.BEGIN in raw and self.END in raw:
            return raw.split(self.BEGIN)[1].split(self.END)[0].strip()

        return raw.strip()

    # -------------------------
    # VALIDATE PYTHON SYNTAX
    # -------------------------
    def validate_syntax(self, code: str) -> Dict:
        try:
            ast.parse(code)
            return {"valid": True}
        except SyntaxError as e:
            return {
                "valid": False,
                "error": str(e)
            }

    # -------------------------
    # FULL CONTRACT CHECK
    # -------------------------
    def verify(self, raw_output: str) -> Dict:
        code = self.extract_code(raw_output)
        syntax = self.validate_syntax(code)

        return {
            "code": code,
            "syntax_valid": syntax["valid"],
            "error": syntax.get("error")
        }