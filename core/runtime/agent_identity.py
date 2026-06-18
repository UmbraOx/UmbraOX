class AgentIdentity:

    def __init__(self, name, role):
        self.name = name
        self.role = role

    def serialize(self):
        return {
            "name": self.name,
            "role": self.role
        }