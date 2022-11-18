from typing import Protocol
from models import Departamento, Usuario



class OccurrenceWriteData(Protocol):
    description: str
    obs: str
    user: Usuario


class OccurrenceLocationData(Protocol):
    departament: Departamento
    uuid: str