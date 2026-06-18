from core.runtime.runtime_code_generator import RuntimeCodeGenerator


def test_runtime_code_generator():

    generator = (
        RuntimeCodeGenerator()
    )

    result = generator.generate_stub(
        "TestClass",
        ["run"]
    )

    assert "class TestClass" in result["code"]
    assert "def run" in result["code"]