import json
from typing import Any

from .psychic import Psychic
from psychics.components import psychic


class Participant:
    def __init__(
        self,
        psychic_type: Psychic,
        name: str,
        guessed_count: int = 0,
        *args,
        **kwargs
    ) -> None:
        if not issubclass(psychic_type, Psychic):
            raise TypeError('Participant type must be Psychic')
        
        if not isinstance(name, str):
            raise TypeError('Participant name must be string')
        
        self._psychic_type = psychic_type.__name__
        self._psychic = psychic_type(*args, **kwargs)
        self._name = name
        self._guessed_count = guessed_count
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def guessed(self) -> int:
        return self._guessed_count
    
    @guessed.setter
    def guessed(self, count: int) -> None:
        if not isinstance(count, int):
            raise TypeError('guessed must be int')
        
        if count < 0:
            raise ValueError('guessed must be positive')
        
        self._guessed_count = count
    
    def make_guess(self) -> Any:
        return self._psychic.make_guess()
