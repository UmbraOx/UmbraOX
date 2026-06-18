import uuid


class IntelligentProposalEngine:

    def generate(self, prompt):

        prompt_lower = prompt.lower()

        proposals = []

        if (
            "gui" in prompt_lower
            or "desktop" in prompt_lower
            or "ui" in prompt_lower
        ):

            proposals.append({
                "id": str(uuid.uuid4())[:8],
                "title": "Desktop UI Runtime",
                "target": "core/ui",
                "type": "feature"
            })

        if (
            "agent" in prompt_lower
            or "multi agent" in prompt_lower
        ):

            proposals.append({
                "id": str(uuid.uuid4())[:8],
                "title": "Recursive Agent System",
                "target": "core/agents",
                "type": "architecture"
            })

        if (
            "runtime" in prompt_lower
            or "orchestration" in prompt_lower
        ):

            proposals.append({
                "id": str(uuid.uuid4())[:8],
                "title": "Persistent Runtime Expansion",
                "target": "core/runtime",
                "type": "runtime"
            })

        if (
            "memory" in prompt_lower
        ):

            proposals.append({
                "id": str(uuid.uuid4())[:8],
                "title": "Persistent Memory Layer",
                "target": "core/runtime/memory",
                "type": "memory"
            })

        if (
            "deployment" in prompt_lower
        ):

            proposals.append({
                "id": str(uuid.uuid4())[:8],
                "title": "Deployment Orchestration",
                "target": "core/runtime/deployment",
                "type": "deployment"
            })

        if not proposals:

            proposals.append({
                "id": str(uuid.uuid4())[:8],
                "title": "General Runtime Upgrade",
                "target": "core/runtime",
                "type": "feature"
            })

        return proposals