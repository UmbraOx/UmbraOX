class RuntimeCodeMutator:
    def inject(self, code, snippet):
        return code + "\n" + snippet