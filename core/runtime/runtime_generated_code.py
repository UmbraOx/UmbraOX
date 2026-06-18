class RuntimeGeneratedCode:

    def build(self, domain):

        class_name = (
            domain.title()
            .replace("_", "")
            .replace(" ", "")
        )

        return {
            "path": f"generated/{domain}_module.py",
            "content":
f'''
class {class_name}Module:

    def run(self):

        return "{domain} online"
'''
        }