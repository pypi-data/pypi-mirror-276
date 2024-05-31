from typing import Optional

from torch import Tensor
from spot_llm.models.spotter import Spotter
from transformers import AutoTokenizer, AutoModelForCausalLM  # type: ignore


class HFSpotter(Spotter):
    def __init__(
        self, model_id: str, token: Optional[str] = None, version: str = "0.3"
    ):
        self.token = token
        self.model_id = model_id

    def initialize(self) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id, token=self.token)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id, token=self.token
        )

    def _get_lazy_logits(
        self,
        inputs: Tensor,
    ) -> Tensor:

        return self.model.generate(
            input_ids=inputs,
            do_sample=False,
            temperature=0.0,
            num_return_sequences=1,
            max_new_tokens=1,
        )
