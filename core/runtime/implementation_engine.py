class ImplementationEngine:

    def create(self, proposal):

        target = proposal.get(
            "target",
            "core/runtime/generated"
        )

        title = proposal.get(
            "title",
            "Generated Feature"
        )

        files = []

        files.append({
            "path": f"{target}/__init__.py",
            "content": "# generated package"
        })

        files.append({
            "path": f"{target}/runtime.py",
            "content": self._runtime_stub(title)
        })

        return {
            "files": files,
            "count": len(files)
        }

    def _runtime_stub(self, title):

        return f'''
class GeneratedRuntime:

    def start(self):

        print(
            "[GENERATED_RUNTIME] {title}"
        )
'''