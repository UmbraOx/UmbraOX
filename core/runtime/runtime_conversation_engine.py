import re


class RuntimeConversationEngine:
    """
    Lightweight intent router.
    """

    def classify(self, text):
        text_l = text.lower()

        if any(k in text_l for k in ["build", "create", "make", "game", "app"]):
            return {"intent": "build"}
        if any(k in text_l for k in ["image", "draw", "render"]):
            return {"intent": "image"}
        if text_l.endswith("?"):
            return {"intent": "question"}

        return {"intent": "general"}

    def needs_clarification(self, text):
        return len(text.split()) < 4

    def respond(self, text):
        intent = self.classify(text)
        return {
            "intent": intent,
            "needs_clarification": self.needs_clarification(text),
            "original": text
        }