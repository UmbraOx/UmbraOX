from core.runtime.runtime_gap_analyzer import (
    RuntimeGapAnalyzer
)


def test_gap_analysis():

    analyzer = RuntimeGapAnalyzer()

    result = analyzer.analyze()

    assert "summary" in result

    assert "priority_missing" in result

    assert isinstance(
        result["priority_missing"],
        list
    )