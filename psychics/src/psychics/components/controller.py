import json

from copy import deepcopy
from typing import List, Tuple, Any
from .participant import Participant
from .psychic import OneValuePsychic, RandomPsychic
from psychics.utils.utils import remove_prefixes


def create_participants():
    p1 = Participant(
        psychic_type=OneValuePsychic, 
        name='Экстрасенс 1', 
        value=77
    )
    p2 = Participant(psychic_type=RandomPsychic, name='Колдун 2')
    return p1, p2


class Controller:
    _SESSION_NAME = 'controller'

    def __init__(self, participants, rounds=[]) -> None:
        self._participants = participants
        self._rounds = rounds
    
    @property
    def participants(self):
        return deepcopy(self._participants)
    
    @property
    def rounds(self):
        return deepcopy(self._rounds)

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def save_to_session(self, request):
        request.session[self._SESSION_NAME] = json.dumps(
            self.toJson(), indent=4
        )

    @staticmethod
    def check_controller_exists(function):
        def wrapper(*args, **kwargs):
            request = args[1]
            session = request.session

            if session.get(Controller._SESSION_NAME) is None:
                participants = create_participants()
                controller = Controller(participants)
                controller.save_to_session(request=request)

            return function(*args, **kwargs)
        return wrapper
    
    @classmethod
    def get_from_session(cls, request):
        data = json.loads(json.loads(request.session[cls._SESSION_NAME]))
        data = remove_prefixes(data)
        
        data['participants'] = [Participant(
            psychic_type=globals()[p['psychic_type']],
            name=p['name'],
            guessed_count=p['guessed_count'],
            **p['psychic']
        ) for p in data['participants']]
        
        controller = Controller(**data)
        return controller

    def check_guess_answered(self):
        if (not len(self._rounds) or (
            self._rounds[-1]['answer'] is not None)
        ):
            return True
        return False

    def make_guess(self):
        guesses = []
        for participant in self._participants:
            guesses.append(participant.make_guess())
        
        round = {
            'answer': None, 
            'guesses': tuple(guesses)
        }

        if self.check_guess_answered():
            self._rounds.append(round)
        else:
            self._rounds[-1] = round
        
    def save_answer(self, answer):
        if self._rounds[-1]['answer'] is not None:
            raise RuntimeError('you must call make_guesses first')

        self._rounds[-1]['answer'] = answer

        for i, guess in enumerate(self._rounds[-1]['guesses']):
            if guess == answer:
                self._participants[i].guessed += 1
