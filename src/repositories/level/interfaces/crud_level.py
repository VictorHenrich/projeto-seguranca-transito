from typing import Protocol
from models import Departamento


class LevelWriteData(Protocol):
    description: str
    level: int
    obs: str


class LevelLocationData(Protocol):
    uuid: str
    departament: Departamento