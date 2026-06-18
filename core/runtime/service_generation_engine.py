class ServiceGenerationEngine:

    def generate(
        self,
        service_name
    ):

        return f'''
class {service_name}Service:

    def start(self):

        return "{service_name} service started"
'''