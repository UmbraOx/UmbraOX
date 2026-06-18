class PythonClassBuilder:

    def build(
        self,
        class_name
    ):

        return f'''
class {class_name}:

    def execute(self):

        return "{class_name} executed"
'''