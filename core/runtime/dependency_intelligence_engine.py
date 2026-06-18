from core.runtime.dependency_graph import DependencyGraph
from core.runtime.import_validator import ImportValidator
from core.runtime.constructor_contracts import ConstructorContracts
from core.runtime.runtime_binding_validator import RuntimeBindingValidator


class DependencyIntelligenceEngine:
    """
    Central brain for dependency safety.
    Used before any self-generated upgrade is applied.
    """

    def __init__(self):
        self.graph_builder = DependencyGraph()
        self.import_validator = ImportValidator()
        self.contracts = ConstructorContracts()
        self.binding_validator = RuntimeBindingValidator()

    def analyze_project(self):
        graph = self.graph_builder.build()

        return {
            "dependency_graph": graph,
            "status": "analyzed",
            "nodes": len(graph)
        }

    def validate_import(self, module_name: str):
        return self.import_validator.validate(module_name)

    def validate_constructor(self, cls, args):
        return self.contracts.validate(cls, args)

    def validate_runtime_call(self, obj, method):
        return self.binding_validator.validate_method(obj, method)