import uuid


class RuntimeSessionPersistence:

    def __init__(self):

        self.sessions = {}

    def save_session(
        self,
        data
    ):

        session_id = str(uuid.uuid4())

        self.sessions[session_id] = data

        return session_id

    def load_session(
        self,
        session_id
    ):

        return self.sessions.get(
            session_id,
            {}
        )