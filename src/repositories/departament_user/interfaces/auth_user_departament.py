from typing import Protocol
from models import Departamento



class AuthUserDepartament(Protocol):
    username: str
    password: str
    departament: Departamento