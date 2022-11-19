from dataclasses import dataclass
from models import Departamento


@dataclass
class LevelRegistration:
    description: str
    level: int
    obs: str


@dataclass
class LevelLocation:
    uuid: str
    departament: Departamento


@dataclass
class LevelUpdate:
    data: LevelRegistration
    location_data: LevelLocation



