from typing import Optional

from spot_llm.models.hf_model import HFSpotter


class Opt125Spotter(HFSpotter):
    def __init__(self, token: Optional[str] = None) -> None:
        super().__init__(model_id="facebook/opt-125m", token=token)
