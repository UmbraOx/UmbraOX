class PythonFunctionBuilder:

    def build(
        self,
        function_name
    ):

        return f'''
def {function_name}():

    return "{function_name} active"
'''