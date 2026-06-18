class RuntimeSkillRegistry:

    def __init__(self):

        self.skills = []

    def register(
        self,
        skill
    ):

        self.skills.append(skill)

    def all(self):

        return self.skills