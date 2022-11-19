from typing import Protocol
from models import Departamento



class IUserDepartamentAuthorization(Protocol):
    username: str
    password: str
    uuid_departament: str