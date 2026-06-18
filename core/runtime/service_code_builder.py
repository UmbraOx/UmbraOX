class ServiceCodeBuilder:

    def build_service(
        self,
        service_name
    ):

        class_name = "".join(
            p.capitalize()
            for p in service_name.split("_")
        )

        code = f'''
class {class_name}Service:

    def initialize(self):

        print("[SERVICE] initialized")
'''

        return {
            "path": f"core/services/{service_name}.py",
            "code": code.strip()
        }