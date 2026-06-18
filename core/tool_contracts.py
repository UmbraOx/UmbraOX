def validate_step(step):
    validated = {
        "id": step.get("id"),
        "action": step.get("action", ""),
        "path": step.get("path", ""),
        "content": step.get("content", ""),
        "raw": step.get("raw", {})
    }

    if validated["action"] == "create_folder":
        validated.pop("content", None)

    return validated


def validate_plan(plan):
    validated_steps = []

    for step in plan.get("steps", []):
        validated_steps.append(
            validate_step(step)
        )

    return {
        "task_id": plan.get("task_id"),
        "project_id": plan.get("project_id", "default"),
        "status": "validated",
        "steps": validated_steps
    }