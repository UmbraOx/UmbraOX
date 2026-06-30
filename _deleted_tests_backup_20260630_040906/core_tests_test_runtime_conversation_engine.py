import pytest
from core.runtime.runtime_conversation_engine import RuntimeConversationEngine, ClassificationResult


@pytest.fixture
def engine():
    return RuntimeConversationEngine()


def test_classify_task(engine):
    r = engine.classify("build me a REST API")
    assert r.intent in ("task", "game_request", "command")


def test_classify_question_capital(engine):
    r = engine.classify("what is the capital of France?")
    assert r.intent == "question"


def test_classify_question_howsit(engine):
    r = engine.classify("hows it going?")
    assert r.intent in ("question", "chat")


def test_classify_game_request(engine):
    r = engine.classify("create a pygame game with a player and enemy")
    assert r.intent == "game_request"


def test_classify_health_command(engine):
    r = engine.classify("check system health")
    assert r.intent in ("command", "question", "chat")


def test_classify_metrics_command(engine):
    r = engine.classify("show me the metrics and stats")
    assert r.intent in ("command", "task")


def test_classify_image_request(engine):
    r = engine.classify("generate an image of a forest at sunset")
    assert r.intent == "image_request"


def test_classify_image_request_2(engine):
    r = engine.classify("create a picture of a dragon")
    assert r.intent == "image_request"


def test_classify_video_request(engine):
    r = engine.classify("create a video animation of ocean waves")
    assert r.intent == "video_request"


def test_classify_video_request_2(engine):
    r = engine.classify("make an animation of a sunset")
    assert r.intent == "video_request"


def test_needs_clarification_vague_game(engine):
    r = engine.classify("make a game")
    assert isinstance(r.needs_clarification, bool)


def test_add_turn(engine):
    engine.add_turn("user", "hello", "input")
    assert len(engine.history) == 1


def test_get_history(engine):
    engine.add_turn("user", "test input", "input")
    history = engine.get_history()
    assert len(history) == 1
    assert history[0]["role"] == "user"


def test_clear_history(engine):
    engine.add_turn("user", "test", "input")
    engine.clear_history()
    assert len(engine.history) == 0


def test_build_game_prompt_has_requirements(engine):
    prompt = engine.build_game_prompt("platformer with player and coins")
    assert "pygame" in prompt.lower()
    assert "boundary" in prompt.lower() or "clamp" in prompt.lower() or "SCREEN_WIDTH" in prompt
    assert "collision" in prompt.lower()
    assert "__main__" in prompt
    assert "main()" in prompt


def test_fallback_answer_umbra(engine):
    answer = engine._fallback_answer("what is umbra?")
    assert len(answer) > 10
    assert any(word in answer.lower() for word in ["umbra", "autonomous", "build", "runtime"])


def test_fallback_answer_capital(engine):
    answer = engine._fallback_answer("what is the capital of the usa")
    assert "Washington" in answer or "D.C." in answer


def test_fallback_answer_time(engine):
    answer = engine._fallback_answer("what time is it?")
    assert "time" in answer.lower() or ":" in answer


def test_fallback_answer_how_are_you(engine):
    answer = engine._fallback_answer("hows it going?")
    assert len(answer) > 5


def test_fallback_answer_general(engine):
    answer = engine._fallback_answer("some completely random question xyz")
    assert isinstance(answer, str)
    assert len(answer) > 5


def test_classification_result_to_dict():
    r = ClassificationResult("task", 0.9, False, [], {"raw": "test"})
    d = r.to_dict()
    assert d["intent"] == "task"
    assert d["confidence"] == 0.9
    assert d["needs_clarification"] is False


def test_context_summary_empty(engine):
    summary = engine.get_context_summary()
    assert "No conversation" in summary


def test_context_summary_with_history(engine):
    engine.add_turn("user", "hello there", "input")
    engine.add_turn("umbra", "hi back", "answer")
    summary = engine.get_context_summary()
    assert "You" in summary or "Umbra" in summary


def test_natural_language_build(engine):
    r = engine.classify("I want to make a game with a dragon and treasure")
    assert r.intent in ("game_request", "task")


def test_natural_language_casual(engine):
    r = engine.classify("hey whats up")
    assert r.intent in ("chat", "question")


def test_conversation_turn_to_dict():
    from core.runtime.runtime_conversation_engine import ConversationTurn
    t = ConversationTurn("user", "hello", "input", {"key": "val"})
    d = t.to_dict()
    assert d["role"] == "user"
    assert d["content"] == "hello"
    assert d["turn_type"] == "input"


def test_pending_clarification_none_by_default(engine):
    assert engine.pending_clarification is None


def test_answer_question_no_llm(engine):
    answer = engine.answer_question("what is the capital of france?")
    assert isinstance(answer, str)
    assert len(answer) > 5


def test_build_image_prompt(engine):
    prompt = engine.build_image_prompt("a red dragon flying over mountains")
    assert "dragon" in prompt


def test_game_request_has_metadata(engine):
    r = engine.classify("write a pygame game with enemies and health")
    if r.intent == "game_request":
        assert "raw" in r.metadata


def test_classify_does_not_crash_empty(engine):
    r = engine.classify("  ")
    assert r.intent in ("chat", "task", "question", "command", "game_request", "image_request", "video_request")