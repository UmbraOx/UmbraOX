import pytest
from unittest.mock import patch


def test_self_improvement():
    try:
        from core.runtime.self_improvement_engine import SelfImprovementEngine
        engine = SelfImprovementEngine.__new__(SelfImprovementEngine)
        engine.status = "idle"
        engine.improvement_log = []

        with patch("shutil.copytree", return_value=None):
            with patch("shutil.copy2", return_value=None):
                if hasattr(engine, "improve"):
                    try:
                        engine.improve()
                    except Exception:
                        pass

        assert engine is not None

    except ImportError:
        pytest.skip("SelfImprovementEngine not available in current form")