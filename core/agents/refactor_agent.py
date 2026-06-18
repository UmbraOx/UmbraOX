from core.runtime.umbra_llm_patch_engine import PatchOrchestrator


class RefactorAgent:

    def __init__(self):
        self.orchestrator = PatchOrchestrator()

    def generate(self, scan_result):

        proposals = []

        for node in scan_result["nodes"]:
            # Only propose improvements for now
            if node.functions:
                patch = self.orchestrator.create_patch(
                    file_path=node.path,
                    intent="improve_code_quality"
                )
                proposals.append(patch)

        return proposals