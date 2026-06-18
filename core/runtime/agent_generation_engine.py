class AgentGenerationEngine:

    def generate(
        self,
        agent_name
    ):

        return f'''
class {agent_name}Agent:

    def execute(self):

        return "{agent_name} agent active"
'''