class RuntimeProjectAnalyzer:
    def analyze(self, indexed_files):
        return {
            "python_files": len(indexed_files),
            "modules": [
                item["name"]
                for item in indexed_files
            ]
        }