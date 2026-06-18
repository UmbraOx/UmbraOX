import uuid


class SystemBlueprintEngine:

    def generate(self, prompt, proposals):

        system_id = str(uuid.uuid4())[:8]

        modules = []

        for proposal in proposals:

            modules.append({
                "id": str(uuid.uuid4())[:8],
                "title": proposal.get("title"),
                "target": proposal.get("target"),
                "type": proposal.get("type"),
                "dependencies": [],
                "execution_group": "core"
            })

        return {
            "system_id": system_id,
            "prompt": prompt,
            "modules": modules,
            "status": "planned"
        }