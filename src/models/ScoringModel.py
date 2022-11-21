from abc import ABC, abstractmethod
from typing import List


class ScoringModel(ABC):
    @abstractmethod
    def predict(self, *args, **kwargs) -> int:
        raise NotImplementedError

    @abstractmethod
    def predict_score(self, *args, **kwargs) -> List[float]:
        raise NotImplementedError
