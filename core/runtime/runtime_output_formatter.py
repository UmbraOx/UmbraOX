from datetime import datetime


class RuntimeOutputFormatter:
    """
    Formats Umbra pipeline outputs into clean, readable summaries.
    Used by CLI, future GUI, and handoff documents.
    """

    def format_run(self, pipeline_run):
        lines = [
            f"RUN: {pipeline_run.run_id}",
            f"STATUS: {pipeline_run.status}",
            f"PROMPT: {pipeline_run.prompt[:80]}",
            f"TASKS: {len(pipeline_run.tasks)}",
            f"STARTED: {pipeline_run.started_at}",
        ]
        if pipeline_run.completed_at:
            lines.append(f"COMPLETED: {pipeline_run.completed_at}")
        if pipeline_run.error:
            lines.append(f"ERROR: {pipeline_run.error}")
        if pipeline_run.written_files:
            lines.append(f"FILES WRITTEN: {len(pipeline_run.written_files)}")
            for f in pipeline_run.written_files:
                lines.append(f"  - {f['file']} ({f['lines']} lines)")
        return "\n".join(lines)

    def format_result(self, orchestration_result):
        status = "OK" if orchestration_result.success else "FAIL"
        lines = [
            f"[{status}] {orchestration_result.task_id}",
        ]
        if orchestration_result.response_content:
            preview = orchestration_result.response_content[:200].replace("\n", " ")
            lines.append(f"  {preview}")
        if not orchestration_result.success:
            err = orchestration_result.metadata.get("error", "unknown")
            lines.append(f"  ERROR: {err[:100]}")
        return "\n".join(lines)

    def format_graph_summary(self, summary):
        lines = [
            f"GRAPH SUMMARY",
            f"  Total nodes  : {summary.get('total', 0)}",
            f"  Complete     : {summary.get('complete', False)}",
            f"  Has failures : {summary.get('has_failures', False)}",
        ]
        by_state = summary.get("by_state", {})
        if by_state:
            lines.append("  By state:")
            for state, count in by_state.items():
                lines.append(f"    {state}: {count}")
        return "\n".join(lines)

    def format_health_report(self, report):
        d = report.to_dict()
        lines = [
            f"HEALTH: {d['overall_status'].upper()}",
            f"  Pass: {d['pass_count']}  Warn: {d['warn_count']}  Fail: {d['fail_count']}",
        ]
        for check in d["checks"]:
            icon = "+" if check["status"] == "pass" else ("!" if check["status"] == "warn" else "x")
            lines.append(f"  {icon} {check['name']}: {check['message'] or check['status']}")
        return "\n".join(lines)

    def format_session_history(self, runs):
        if not runs:
            return "No runs in session."
        lines = ["SESSION HISTORY"]
        for r in runs:
            files = len(r.get("written_files", []))
            lines.append(
                f"  {r.get('run_id')} | {r.get('status')} | "
                f"files:{files} | {r.get('prompt', '')[:50]}"
            )
        return "\n".join(lines)