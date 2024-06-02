from spot_llm.models.hf_model import HFSpotter


class MistralSpotter(HFSpotter):
    def __init__(self, token: str, version: str = "0.3"):
        super().__init__(model_id=f"mistralai/Mistral-7B-v{version}", token=token)
