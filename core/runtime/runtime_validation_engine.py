import ast
import os
from datetime import datetime


class ValidationResult:

    def __init__(self, passed, errors=None, warnings=None, metadata=None):
        self.passed = passed
        self.errors = errors or []
        self.warnings = warnings or []
        self.metadata = metadata or {}
        self.validated_at = datetime.now().isoformat()

    def to_dict(self):
        return {
            "passed": self.passed,
            "errors": self.errors,
            "warnings": self.warnings,
            "metadata": self.metadata,
            "validated_at": self.validated_at,
        }


class RuntimeValidationEngine:
    """
    Code and execution output validation.
    - Python syntax validation
    - Output schema validation
    - File existence validation
    - Custom rule validation
    - Validation history
    """

    def __init__(self):
        self.validation_history = []
        self.custom_rules = {}

    def validate_python_syntax(self, code, label="unknown"):
        errors = []
        warnings = []
        try:
            ast.parse(code)
        except SyntaxError as e:
            errors.append(f"SyntaxError at line {e.lineno}: {e.msg}")
        except Exception as e:
            errors.append(f"ParseError: {str(e)}")

        if not code.strip():
            warnings.append("Code is empty or whitespace only")

        lines = code.splitlines()
        if len(lines) > 1000:
            warnings.append(f"Large file: {len(lines)} lines")

        result = ValidationResult(
            passed=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            metadata={"label": label, "line_count": len(lines)},
        )
        self._record(result)
        return result

    def validate_file_exists(self, path, label="file_check"):
        exists = os.path.exists(path)
        result = ValidationResult(
            passed=exists,
            errors=[] if exists else [f"File not found: {path}"],
            metadata={"label": label, "path": path},
        )
        self._record(result)
        return result

    def validate_output_schema(self, output, required_keys, label="output"):
        errors = []
        if not isinstance(output, dict):
            errors.append(f"Expected dict, got {type(output).__name__}")
        else:
            for key in required_keys:
                if key not in output:
                    errors.append(f"Missing required key: '{key}'")
        result = ValidationResult(
            passed=len(errors) == 0,
            errors=errors,
            metadata={"label": label, "required_keys": required_keys},
        )
        self._record(result)
        return result

    def validate_string_not_empty(self, value, label="string"):
        passed = isinstance(value, str) and len(value.strip()) > 0
        result = ValidationResult(
            passed=passed,
            errors=[] if passed else ["Value is empty or not a string"],
            metadata={"label": label},
        )
        self._record(result)
        return result

    def validate_python_file(self, file_path):
        if not os.path.exists(file_path):
            result = ValidationResult(False, errors=[f"File not found: {file_path}"])
            self._record(result)
            return result
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
        return self.validate_python_syntax(code, label=file_path)

    def register_custom_rule(self, rule_name, rule_fn):
        """Register a custom validation rule: fn(value) -> (passed: bool, message: str)"""
        self.custom_rules[rule_name] = rule_fn

    def validate_custom(self, rule_name, value):
        if rule_name not in self.custom_rules:
            raise KeyError(f"No custom rule: {rule_name}")
        passed, message = self.custom_rules[rule_name](value)
        result = ValidationResult(
            passed=passed,
            errors=[] if passed else [message],
            metadata={"rule": rule_name},
        )
        self._record(result)
        return result

    def validate_all_python_files(self, directory):
        results = []
        for root, dirs, files in os.walk(directory):
            for fname in files:
                if fname.endswith(".py"):
                    full_path = os.path.join(root, fname)
                    results.append((full_path, self.validate_python_file(full_path)))
        failed = [(p, r) for p, r in results if not r.passed]
        return {
            "total": len(results),
            "passed": len(results) - len(failed),
            "failed": len(failed),
            "failures": [{"path": p, "errors": r.errors} for p, r in failed],
        }

    def get_history(self):
        return list(self.validation_history)

    def get_failed_validations(self):
        return [r for r in self.validation_history if not r["passed"]]

    def _record(self, result):
        self.validation_history.append(result.to_dict())