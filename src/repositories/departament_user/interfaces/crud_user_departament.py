from typing import Protocol
from models import Departamento



class UserDepartamentLocationData(Protocol):
    uuid: str
    departament: Departamento



class UserDepartamentWriteData(Protocol):
    name: str
    user: str
    password: str
    office: str
    