from dataclasses import dataclass
from typing import Optional
from abc import ABC



@dataclass
class LevelData(ABC):
    descricao: str
    nivel: int
    obs: Optional[str]



@dataclass
class LevelRegistration(LevelData):
    pass



@dataclass
class LevelView(LevelData):
    uuid: str
    





