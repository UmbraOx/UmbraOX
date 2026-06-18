class MessageBus:

    def __init__(self):
        self.messages = []

    def send(self, sender, receiver, content):
        msg = {
            "from": sender,
            "to": receiver,
            "content": content
        }
        self.messages.append(msg)

    def broadcast(self, sender, content):
        self.messages.append({
            "from": sender,
            "to": "all",
            "content": content
        })

    def get_messages_for(self, agent_name):
        return [
            m for m in self.messages
            if m["to"] == agent_name or m["to"] == "all"
        ]

    def clear_for(self, agent_name):
        self.messages = [
            m for m in self.messages
            if m["to"] not in [agent_name, "all"]
        ]