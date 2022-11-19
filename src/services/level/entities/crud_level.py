from dataclasses import dataclass
from typing import Optional
from models import Departamento


@dataclass
class LevelRegistration:
    description: str
    level: int
    obs: str
    departament: Optional[Departamento] = None


@dataclass
class LevelLocation:
    uuid: str
    departament: Departamento


@dataclass
class LevelUpdate:
    data: LevelRegistration
    location_data: LevelLocation



