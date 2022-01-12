from abc import ABC, abstractmethod
from random import randint
from typing import Any


class Psychic(ABC):
    @abstractmethod
    def make_guess(self) -> Any:
        pass


class TwoDigitPsychic(Psychic):
    _START_RANGE = 10
    _END_RANGE = 100


class RandomPsychic(TwoDigitPsychic):
    def make_guess(self) -> int:
        return randint(self._START_RANGE, self._END_RANGE)


class OneValuePsychic(TwoDigitPsychic):
    def __init__(self, value: int) -> None:
        if self._START_RANGE <= value < self._END_RANGE:
            self._value = value
        else:
            raise ValueError('value out of range')

    def make_guess(self) -> int:
        return self._value
