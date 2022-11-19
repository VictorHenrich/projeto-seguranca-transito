from typing import Protocol, Optional
from models import Departamento, Usuario



class IOccurrenceRegistration(Protocol):
    description: str
    obs: str
    user: Optional[Usuario]
    departament: Optional[Departamento]


class IOccurrenceLocation(Protocol):
    departament: Departamento
    uuid: Optional[str]