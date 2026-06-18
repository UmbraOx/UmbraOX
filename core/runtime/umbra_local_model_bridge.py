class UmbraLocalModelBridge:

    def generate(
        self,
        prompt
    ):
        return {
            "prompt": prompt,
            "response": "local_model_stub_response"
        }