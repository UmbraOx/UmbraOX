# core/runtime/improvement_planner.py


class ImprovementPlanner:

    def generate_plan(self, review_result):

        suggestions = review_result.get(
            "suggestions",
            []
        )

        plans = []

        for suggestion in suggestions:

            # -----------------------------------------
            # TODO IMPROVEMENTS
            # -----------------------------------------

            if "TODO" in suggestion:

                plans.append({
                    "type": "maintenance",
                    "priority": "medium",
                    "goal": "Resolve TODO items",
                    "reason": suggestion
                })

            # -----------------------------------------
            # IMPORT COMPLEXITY
            # -----------------------------------------

            elif "imports" in suggestion.lower():

                plans.append({
                    "type": "architecture",
                    "priority": "high",
                    "goal": "Reduce import complexity",
                    "reason": suggestion
                })

            # -----------------------------------------
            # SMALL PROJECT
            # -----------------------------------------

            elif "small" in suggestion.lower():

                plans.append({
                    "type": "growth",
                    "priority": "low",
                    "goal": "Expand project systems",
                    "reason": suggestion
                })

        print(
            f"[IMPROVEMENT_PLANNER] "
            f"{len(plans)} plans created"
        )

        return plans