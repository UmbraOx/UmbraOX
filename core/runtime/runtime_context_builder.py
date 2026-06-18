from datetime import datetime


class RuntimeContext:

    def __init__(self):
        self.system_prompt = ""
        self.objective = ""
        self.memory_entries = []
        self.task_history = []
        self.current_files = {}
        self.agent_role = "autonomous_executor"
        self.metadata = {}
        self.built_at = datetime.now().isoformat()

    def to_prompt_string(self, max_memory=10, max_history=5):
        parts = []

        if self.system_prompt:
            parts.append(f"[SYSTEM]\n{self.system_prompt}")

        if self.agent_role:
            parts.append(f"[ROLE]\nYou are an {self.agent_role}.")

        if self.objective:
            parts.append(f"[OBJECTIVE]\n{self.objective}")

        if self.memory_entries:
            recent = self.memory_entries[-max_memory:]
            parts.append("[MEMORY]\n" + "\n".join(f"- {m}" for m in recent))

        if self.task_history:
            recent_tasks = self.task_history[-max_history:]
            parts.append("[TASK HISTORY]\n" + "\n".join(
                f"- [{t['state']}] {t['task_id']}" for t in recent_tasks
            ))

        if self.current_files:
            file_list = "\n".join(f"- {k}" for k in list(self.current_files.keys())[:20])
            parts.append(f"[CURRENT FILES]\n{file_list}")

        if self.metadata:
            meta_str = "\n".join(f"  {k}: {v}" for k, v in self.metadata.items())
            parts.append(f"[METADATA]\n{meta_str}")

        return "\n\n".join(parts)

    def to_dict(self):
        return {
            "system_prompt": self.system_prompt,
            "objective": self.objective,
            "memory_entries": self.memory_entries,
            "task_history": self.task_history,
            "current_files": list(self.current_files.keys()),
            "agent_role": self.agent_role,
            "metadata": self.metadata,
            "built_at": self.built_at,
        }


class RuntimeContextBuilder:
    """
    Assembles LLM context from memory, task history, files, and objectives.
    Produces RuntimeContext objects ready for injection into LLM calls.
    """

    def __init__(self, memory_bridge=None, task_state_machine=None):
        self.memory_bridge = memory_bridge
        self.task_state_machine = task_state_machine
        self.base_system_prompt = (
            "You are Umbra, an autonomous AI runtime. "
            "You plan, execute, validate, and improve software systems. "
            "Be precise, structured, and always produce actionable output."
        )

    def build(self, objective, agent_role=None, extra_metadata=None):
        ctx = RuntimeContext()
        ctx.system_prompt = self.base_system_prompt
        ctx.objective = objective
        ctx.agent_role = agent_role or "autonomous_executor"

        if self.memory_bridge:
            try:
                entries = self.memory_bridge.retrieve(objective)
                ctx.memory_entries = [str(e) for e in entries[:15]]
            except Exception:
                pass

        if self.task_state_machine:
            try:
                all_tasks = self.task_state_machine.get_all_tasks()
                ctx.task_history = [
                    {"task_id": t.task_id, "state": t.state}
                    for t in all_tasks[-10:]
                ]
            except Exception:
                pass

        if extra_metadata:
            ctx.metadata.update(extra_metadata)

        ctx.metadata["objective_length"] = len(objective)
        ctx.metadata["context_built_at"] = datetime.now().isoformat()

        return ctx

    def build_coder_context(self, objective, existing_code=None, error_output=None):
        ctx = self.build(objective, agent_role="code_generator")
        if existing_code:
            ctx.current_files["current_code"] = existing_code
            ctx.metadata["has_existing_code"] = True
        if error_output:
            ctx.metadata["last_error"] = error_output[:500]
        return ctx

    def build_planner_context(self, objective, known_tasks=None):
        ctx = self.build(objective, agent_role="task_planner")
        if known_tasks:
            ctx.task_history = [{"task_id": t, "state": "known"} for t in known_tasks]
        return ctx

    def build_validator_context(self, objective, test_output=None):
        ctx = self.build(objective, agent_role="validator")
        if test_output:
            ctx.metadata["test_output_preview"] = test_output[:500]
        return ctx

    def set_system_prompt(self, prompt):
        self.base_system_prompt = prompt

    def inject_files(self, context, file_dict):
        """Add file contents directly into an existing context."""
        context.current_files.update(file_dict)
        return context