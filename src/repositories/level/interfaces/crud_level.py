from typing import Protocol, Optional
from models import Departamento


class ILevelRegistration(Protocol):
    description: str
    level: int
    obs: str
    departament: Optional[Departamento]


class ILevelLocation(Protocol):
    uuid: str
    departament: Departamento