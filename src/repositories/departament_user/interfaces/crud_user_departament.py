from typing import Protocol, Optional
from models import Departamento



class IUserDepartamentLocation(Protocol):
    uuid: str
    departament: Departamento



class IUserDepartamentRegistration(Protocol):
    name: str
    user: str
    password: str
    office: str
    departament: Optional[Departamento]
    