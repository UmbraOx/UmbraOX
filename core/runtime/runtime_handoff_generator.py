import json
import os
from datetime import datetime


class RuntimeHandoffGenerator:
    """
    Generates handoff documents so Umbra can resume across sessions/chats.
    Produces both machine-readable JSON and human-readable markdown.
    """

    def __init__(self, base_dir=None):
        self.base_dir = base_dir or os.getcwd()

    def generate(self, runtime_components, output_path=None):
        handoff = self._build_handoff(runtime_components)
        output_path = output_path or os.path.join(
            self.base_dir, "sessions", f"handoff_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(handoff, f, indent=2)
        return output_path, handoff

    def generate_markdown(self, runtime_components, output_path=None):
        _, handoff = self.generate(runtime_components)
        md = self._build_markdown(handoff)
        md_path = output_path or os.path.join(
            self.base_dir, "sessions", f"handoff_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        )
        os.makedirs(os.path.dirname(md_path), exist_ok=True)
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md)
        return md_path, md

    def _build_handoff(self, runtime_components):
        pipeline = runtime_components.get("pipeline")
        graph = runtime_components.get("graph")
        state_machine = runtime_components.get("state_machine")
        llm = runtime_components.get("llm")

        runs = pipeline.get_run_history() if pipeline else []
        graph_summary = graph.summary() if graph else {}
        sm_summary = state_machine.summary() if state_machine else {}

        recent_runs = runs[-10:] if runs else []
        last_run = runs[-1] if runs else None

        return {
            "generated_at": datetime.now().isoformat(),
            "umbra_version": "Runtime Core v2",
            "llm_provider": llm.get_provider() if llm else "unknown",
            "llm_model": llm.get_model() if llm else "unknown",
            "session_stats": {
                "total_runs": len(runs),
                "graph_nodes": graph_summary.get("total", 0),
                "registered_tasks": sm_summary.get("total", 0),
            },
            "last_run": last_run,
            "recent_runs": recent_runs,
            "graph_summary": graph_summary,
            "state_machine_summary": sm_summary,
            "next_steps": self._infer_next_steps(runs, graph_summary),
        }

    def _infer_next_steps(self, runs, graph_summary):
        steps = []
        if not runs:
            steps.append("No runs completed yet — start with a prompt")
        else:
            failed = sum(1 for r in runs if r.get("status") == "completed_with_failures")
            if failed:
                steps.append(f"{failed} run(s) had failures — type 'resume' to retry")
            completed = sum(1 for r in runs if r.get("status") == "completed")
            steps.append(f"{completed} run(s) completed successfully")

        if graph_summary.get("has_failures"):
            steps.append("Execution graph has failed nodes — review workspace results")

        return steps

    def _build_markdown(self, handoff):
        lines = [
            "# UMBRA HANDOFF DOCUMENT",
            f"Generated: {handoff['generated_at']}",
            f"Version: {handoff['umbra_version']}",
            "",
            "## LLM Configuration",
            f"- Provider: {handoff['llm_provider']}",
            f"- Model: {handoff['llm_model']}",
            "",
            "## Session Stats",
            f"- Total runs: {handoff['session_stats']['total_runs']}",
            f"- Graph nodes: {handoff['session_stats']['graph_nodes']}",
            f"- Registered tasks: {handoff['session_stats']['registered_tasks']}",
            "",
            "## Next Steps",
        ]
        for step in handoff.get("next_steps", []):
            lines.append(f"- {step}")

        if handoff.get("recent_runs"):
            lines += ["", "## Recent Runs"]
            for r in handoff["recent_runs"][-5:]:
                files = len(r.get("written_files", []))
                lines.append(f"- {r.get('run_id')} | {r.get('status')} | files:{files} | {r.get('prompt','')[:60]}")

        return "\n".join(lines)