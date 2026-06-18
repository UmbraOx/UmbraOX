import ast
from pathlib import Path
from typing import Dict, List


class UmbraASTAnalyzer:
    """
    Static AST-based code intelligence layer
    """

    def analyze_file(self, file_path: str) -> Dict:
        path = Path(file_path)
        code = path.read_text(encoding="utf-8", errors="ignore")

        tree = ast.parse(code)

        functions = []
        classes = []
        imports = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)

            if isinstance(node, ast.ClassDef):
                classes.append(node.name)

            if isinstance(node, ast.Import):
                for n in node.names:
                    imports.append(n.name)

            if isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)

        return {
            "file": file_path,
            "functions": functions,
            "classes": classes,
            "imports": imports,
            "function_count": len(functions),
            "class_count": len(classes)
        }

    def scan_project(self, root: str) -> List[Dict]:
        root_path = Path(root)
        results = []

        for file in root_path.rglob("*.py"):
            try:
                results.append(self.analyze_file(str(file)))
            except Exception:
                continue

        return results