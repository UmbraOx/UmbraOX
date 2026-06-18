class SourceCodeSynthesizer:

    def synthesize_class(
        self,
        class_name
    ):

        return f'''
class {class_name}:

    def run(self):

        return "{class_name} active"
'''