from core.runtime.runtime_prompt_ingestor import RuntimePromptIngestor


def test_runtime_prompt_ingestor():

    ingestor = RuntimePromptIngestor()

    result = ingestor.ingest(
        "build a planner"
    )

    assert result["status"] == "ingested"