from core.runtime.umbra_unified_runtime import (
    UmbraUnifiedRuntime
)

from core.runtime.umbra_autonomous_company import (
    UmbraAutonomousCompany
)

from core.runtime.umbra_runtime_persistence import (
    UmbraRuntimePersistence
)

from core.runtime.umbra_self_expansion_engine import (
    UmbraSelfExpansionEngine
)


class UmbraContinuousRuntime:

    def __init__(self):
        self.runtime = (
            UmbraUnifiedRuntime()
        )

        self.company = (
            UmbraAutonomousCompany()
        )

        self.persistence = (
            UmbraRuntimePersistence()
        )

        self.expansion = (
            UmbraSelfExpansionEngine()
        )

    def boot(self):
        return self.runtime.boot()

    def execute(
        self,
        objective
    ):
        runtime_result = (
            self.runtime.execute(
                objective
            )
        )

        company_result = (
            self.company.operate(
                objective
            )
        )

        expanded = (
            self.expansion.expand({
                "runtime": runtime_result,
                "company": company_result
            })
        )

        self.persistence.save(
            expanded
        )

        return expanded