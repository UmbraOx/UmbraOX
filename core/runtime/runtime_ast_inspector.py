import ast


class RuntimeASTInspector:

    def inspect(
        self,
        content
    ):

        try:

            ast.parse(content)

            return True

        except Exception:

            return False