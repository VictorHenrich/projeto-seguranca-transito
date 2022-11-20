from typing import Protocol
from models import Nivel, Departamento



class IOccurrenceTypeRegistration(Protocol):
    description: str
    instruction: str
    level: Nivel



class IOccurrenceTypeLocation(Protocol):
    uuid: str


class IOccurrenceTypeListing(Protocol):
    departament: Departamento
    