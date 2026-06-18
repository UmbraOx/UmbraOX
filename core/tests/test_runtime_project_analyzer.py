from core.runtime.runtime_codebase_indexer import (
    RuntimeCodebaseIndexer,
)

from core.runtime.runtime_project_analyzer import (
    RuntimeProjectAnalyzer,
)


def test_runtime_project_analyzer():
    indexer = RuntimeCodebaseIndexer()

    indexed = indexer.index("core")

    analyzer = RuntimeProjectAnalyzer()

    result = analyzer.analyze(indexed)

    assert "python_files" in result