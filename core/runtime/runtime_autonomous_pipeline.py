import json
import os
from datetime import datetime


class PipelineRun:
    def __init__(self, run_id, prompt):
        self.run_id = run_id
        self.prompt = prompt
        self.status = "initializing"
        self.tasks = []
        self.results = []
        self.written_files = []
        self.started_at = datetime.now().isoformat()
        self.completed_at = None
        self.error = None

    def to_dict(self):
        return {
            "run_id": self.run_id,
            "prompt": self.prompt,
            "status": self.status,
            "tasks": self.tasks,
            "results": [
                r.to_dict() if hasattr(r, "to_dict") else str(r)
                for r in self.results
            ],
            "written_files": self.written_files,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "error": self.error,
        }


PLANNER_SYSTEM_PROMPT = (
    "You are Umbra's task planner.\n"
    "Break objectives into 3-6 executable steps.\n\n"
    "Return ONLY valid JSON:\n"
    "{\n"
    '  "tasks": [\n'
    '    {"task_id": "task_1", "description": "...", "depends_on": []}\n'
    "  ]\n"
    "}\n"
)

CODER_SYSTEM_PROMPT = (
    "You are Umbra's code generator.\n"
    "Generate clean, complete, runnable Python code.\n"
    "Always include imports, main entry point, and error handling.\n"
    "Return code inside a Python code block."
)


class RuntimeAutonomousPipeline:
    """
    Prompt → plan → execute → extract code → write workspace files.
    Fully compatible with Umbra orchestrator + workspace system.
    """

    def __init__(
        self,
        llm_orchestrator,
        workspace_manager,
        validation_engine,
        session_persistence=None,
        code_extractor=None,
        code_writer=None,
    ):
        self.orchestrator = llm_orchestrator
        self.workspace = workspace_manager
        self.validator = validation_engine
        self.persistence = session_persistence

        self.run_history = []
        self._run_counter = 0

        # Code extractor (safe fallback if missing)
        if code_extractor is None:
            from core.runtime.runtime_code_extractor import RuntimeCodeExtractor
            self.extractor = RuntimeCodeExtractor()
        else:
            self.extractor = code_extractor

        self.code_writer = code_writer

        # Optional prompt templates
        try:
            from core.runtime.runtime_prompt_templates import RuntimePromptTemplates
            self.prompt_templates = RuntimePromptTemplates()
        except Exception:
            self.prompt_templates = None

    # =========================
    # MAIN ENTRY
    # =========================
    def run(self, prompt, workspace_id=None):
        self._run_counter += 1
        run_id = f"run_{self._run_counter:04d}"
        ws_id = workspace_id or run_id

        pipeline_run = PipelineRun(run_id, prompt)

        try:
            ws = self.workspace.create_workspace(ws_id)
            pipeline_run.status = "planning"

            # 1. PLAN
            task_plan = self._plan_tasks(prompt)
            pipeline_run.tasks = task_plan

            ws.write_file(
                "task_plan.json",
                json.dumps(task_plan, indent=2),
            )

            if not task_plan:
                raise RuntimeError("Task planner returned empty plan")

            # 2. EXECUTE TASKS
            pipeline_run.status = "executing"

            for task_def in task_plan:
                task_id = f"{run_id}_{task_def['task_id']}"
                objective = task_def["description"]
                deps = task_def.get("depends_on", [])

                system_prompt = self._get_system_prompt(objective)

                result = self.orchestrator.orchestrate(
                    task_id=task_id,
                    objective=objective,
                    system_prompt=system_prompt,
                    dependencies=deps,
                    extra_metadata={
                        "run_id": run_id,
                        "original_prompt": prompt[:200],
                    },
                )

                pipeline_run.results.append(result)

                # 3. EXTRACT CODE
                if getattr(result, "success", False) and getattr(result, "response_content", None):
                    written = self._extract_and_write_code(
                        result.response_content,
                        task_id,
                        ws,
                    )
                    pipeline_run.written_files.extend(written)

                ws.write_file(
                    f"results/{task_id}.json",
                    json.dumps(result.to_dict(), indent=2),
                )

            # 4. FINALIZE
            pipeline_run.status = "validating"

            graph_summary = self.orchestrator.get_graph_summary()
            ws.write_file(
                "graph_summary.json",
                json.dumps(graph_summary, indent=2),
            )

            ws.write_file(
                "written_files.json",
                json.dumps(pipeline_run.written_files, indent=2),
            )

            failed = graph_summary.get("by_state", {}).get("failed", 0)
            pipeline_run.status = (
                "completed" if failed == 0 else "completed_with_failures"
            )

        except Exception as e:
            pipeline_run.status = "failed"
            pipeline_run.error = str(e)

        finally:
            pipeline_run.completed_at = datetime.now().isoformat()

        # 5. PERSIST
        if self.persistence:
            try:
                self.persistence.save(
                    f"pipeline_runs/{pipeline_run.run_id}.json",
                    pipeline_run.to_dict(),
                )
            except Exception:
                pass

        self.run_history.append(pipeline_run)
        return pipeline_run

    # =========================
    # PLANNING
    # =========================
    def _plan_tasks(self, prompt):
        if not self.orchestrator.llm.is_configured():
            return self._default_task_plan(prompt)

        response = self.orchestrator.llm.complete(
            prompt=f"Objective:\n{prompt}",
            system_prompt=PLANNER_SYSTEM_PROMPT,
            temperature=0.3,
            max_tokens=900,
        )

        if not response.success:
            return self._default_task_plan(prompt)

        try:
            raw = response.content.strip()

            # Clean markdown if present
            if "```" in raw:
                raw = raw.split("```")
                raw = raw[1] if len(raw) > 1 else raw[0]
                raw = raw.replace("json", "").strip()

            data = json.loads(raw)
            tasks = data.get("tasks", [])

            if isinstance(tasks, list) and tasks:
                return tasks

        except Exception:
            pass

        return self._default_task_plan(prompt)

    # =========================
    # CODE EXTRACTION + WRITE
    # =========================
    def _extract_and_write_code(self, response_content, task_id, workspace):
        written = []

        blocks = self.extractor.extract_python_blocks(
            response_content,
            source_hint=task_id,
        )

        for i, block in enumerate(blocks):
            code = block.content.strip()

            if len(code) < 15:
                continue

            validation = self.validator.validate_python_syntax(
                code,
                label=task_id,
            )

            if not validation.passed:
                continue

            suffix = f"_{i}" if i > 0 else ""
            filename = f"code/{task_id}{suffix}.py"

            try:
                workspace.write_file(filename, code + "\n")

                written.append({
                    "file": filename,
                    "task_id": task_id,
                    "lines": getattr(block, "line_count", len(code.splitlines())),
                })

                if self.code_writer:
                    try:
                        self.code_writer.write(
                            f"generated/{task_id}{suffix}.py",
                            code + "\n",
                        )
                    except Exception:
                        pass

            except Exception:
                continue

        return written

    # =========================
    # SYSTEM PROMPTS
    # =========================
    def _get_system_prompt(self, objective):
        if self.prompt_templates:
            try:
                return self.prompt_templates.get_prompt(objective)
            except Exception:
                pass
        return CODER_SYSTEM_PROMPT

    # =========================
    # FALLBACK PLAN
    # =========================
    def _default_task_plan(self, prompt):
        return [
            {
                "task_id": "task_1",
                "description": f"Analyze requirement: {prompt}",
                "depends_on": [],
            },
            {
                "task_id": "task_2",
                "description": f"Implement solution: {prompt}",
                "depends_on": ["task_1"],
            },
            {
                "task_id": "task_3",
                "description": f"Validate and finalize: {prompt}",
                "depends_on": ["task_2"],
            },
        ]

    # =========================
    # HISTORY + UTIL
    # =========================
    def get_run_history(self):
        return [r.to_dict() for r in self.run_history]

    def get_last_run(self):
        return self.run_history[-1] if self.run_history else None

    def get_run_by_id(self, run_id):
        for run in self.run_history:
            if run.run_id == run_id:
                return run
        return None