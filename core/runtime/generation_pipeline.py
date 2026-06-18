class GenerationPipeline:

    def generate(self, proposals):

        generated = []

        for proposal in proposals:

            path = (
                f"generated/"
                f"{proposal['type']}_module.py"
            )

            content = f'''
class {proposal["type"].title()}Module:

    def run(self):

        return "{proposal["type"]} active"
'''

            generated.append({
                "path": path,
                "content": content
            })

        return generated