from typing import NamedTuple
from enum import Enum

class Player(NamedTuple):
    label: str
    color: str

class Move(NamedTuple):
    row: int
    col: int
    label: str=""

class Opponent(Enum):
    HUMAN = 0
    VALUE_ITERATION = 1
    POLICY_ITERATION = 2