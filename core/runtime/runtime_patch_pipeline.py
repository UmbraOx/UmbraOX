class RuntimePatchPipeline:
    def process(self, patches):
        return {
            "processed": len(patches),
            "success": True,
        }