from core.runtime.runtime_session_persistence import RuntimeSessionPersistence


def test_runtime_session_persistence():

    engine = RuntimeSessionPersistence()

    session_id = engine.save_session(
        {"goal": "build"}
    )

    loaded = engine.load_session(
        session_id
    )

    assert loaded["goal"] == "build"