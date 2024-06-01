from abc import abstractmethod
from typing import Any, List, Optional, Tuple

import numpy as np
from torch import Tensor


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

    @abstractmethod
    def tokenize(self, text: str) -> Tensor:
        raise NotImplementedError()

    @abstractmethod
    def _get_lazy_logits(
        self,
        inputs: Tensor,
    ) -> Tensor:
        raise NotImplementedError()

    def score(self, text: str, num_tokens: int = 24) -> float:

        outputs, tokenz = self.predict_logits_and_tokenz(text)

        output = outputs[0][0]
        rankings: List[int] = []
        for i in range(output.shape[0] - 1):
            if i < num_tokens:
                continue
            logit = output[i + 1, :]
            actual_token = tokenz[0, i]
            rankings.append(int((logit > logit[actual_token]).sum().item()))

        if len(rankings) == 0:
            return -1.0
        return float(np.mean(rankings) / output.shape[1])

    def is_human(self, text: str, treshold: float = 0.1) -> bool:
        return self.score(text) >= treshold
