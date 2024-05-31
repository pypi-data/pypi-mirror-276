import numpy as np
from torch import Tensor


from abc import abstractmethod
from typing import Any, List, Optional, Tuple


class Spotter:
    def __init__(
        self,
        model_id: str,
        token: Optional[str] = None,
        base_token_count: int = 24,
    ) -> None:
        self.model_id = model_id
        self.token = token
        self.base_token_count = base_token_count
        self.tokenizer: Any
        self.model: Any
        self.initialize()

    @abstractmethod
    def initialize(self) -> None:
        raise NotImplementedError()

    def predict_logits_and_tokenz(self, input_prompt: str) -> Tuple[Tensor, Tensor]:
        tokenz = self.tokenize(input_prompt)
        return self._get_lazy_logits(tokenz), tokenz

    def tokenize(self, text: str) -> Tensor:
        tokenz = self.tokenizer.encode(text, add_special_tokens=False)
        return tokenz

    @abstractmethod
    def _get_lazy_logits(
        self,
        inputs: Tensor,
    ) -> Tensor:
        raise NotImplementedError()

    def score(self, text: str) -> float:

        outputs, tokenz = self.predict_logits_and_tokenz(text)

        output = outputs[0][0]
        rankings: List[int] = []
        for i in range(output.shape[0] - 1):
            logit = output[i + 1, :]
            actual_token = tokenz[0, i]
            rankings.append(int((logit > logit[actual_token]).sum().item()))

        return float(np.mean(rankings))

    def is_human(self, text: str, treshold: float = 0.1) -> bool:
        return self.score(text) >= treshold
