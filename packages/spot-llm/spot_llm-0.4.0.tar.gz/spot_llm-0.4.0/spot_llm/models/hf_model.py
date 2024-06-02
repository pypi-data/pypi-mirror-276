from typing import Optional

import torch
from torch import Tensor
from transformers import AutoTokenizer, AutoModelForCausalLM  # type: ignore

from spot_llm.models.spotter import Spotter


class HFSpotter(Spotter):
    def __init__(self, model_id: str, token: Optional[str] = None):
        torch.set_default_dtype(torch.float16)
        super().__init__(model_id=model_id, token=token)

    def initialize(self) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id, token=self.token)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id, token=self.token, device_map="auto"
        )

    def tokenize(self, text: str) -> Tensor:
        tokenz = self.tokenizer(
            text, add_special_tokens=False, return_tensors="pt"
        ).input_ids
        return tokenz

    def _get_lazy_logits(
        self,
        inputs: Tensor,
    ) -> Tensor:
        with torch.no_grad():
            output = self.model(inputs.to(self.model.device))
        return output
