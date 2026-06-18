from datetime import datetime


class OrchestrationResult:
    def __init__(self, success, task_id, response, context, metadata=None):
        self.success = success
        self.task_id = task_id
        self.response_content = response
        self.context_used = context
        self.metadata = metadata or {}
        self.created_at = datetime.now().isoformat()

    def to_dict(self):
        return self.__dict__


class RuntimeLLMOrchestrator:
    """
    Stable orchestration pipeline:
    context → LLM → validate → graph/state updates
    """

    def __init__(self, llm, context_builder, graph, state_machine, validator=None):
        self.llm = llm
        self.context = context_builder
        self.graph = graph
        self.state = state_machine
        self.validator = validator
        self.history = []

    def orchestrate(self, task_id, objective):
        if task_id not in self.state.tasks:
            self.state.register(task_id, {"objective": objective})

        self.graph.add_node(task_id, {"objective": objective})

        try:
            ctx = self.context.build(objective=objective)

            response = self.llm.complete(
                prompt=objective,
                system_prompt=getattr(ctx, "system_prompt", None),
            )

            if not response.success:
                raise RuntimeError(response.error)

            if self.validator:
                v = self.validator.validate_string_not_empty(response.content, task_id)
                if not v.passed:
                    raise RuntimeError("Empty response")

            self.state.complete(task_id, result=response.content)
            self.graph.mark_node_completed(task_id, result=response.content)

            result = OrchestrationResult(
                True,
                task_id,
                response.content,
                str(ctx.__dict__)
            )

        except Exception as e:
            self.state.fail(task_id, str(e))
            self.graph.mark_node_failed(task_id, str(e))

            result = OrchestrationResult(False, task_id, "", "", {"error": str(e)})

        self.history.append(result.to_dict())
        return result