class RuntimeFailurePipeline:

    def process(self, error):

        return {
            "failure": str(error),
            "handled": True
        }