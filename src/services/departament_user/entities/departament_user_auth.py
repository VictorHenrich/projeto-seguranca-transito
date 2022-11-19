from dataclasses import dataclass


@dataclass
class DepartamentUserAuthorization:
    username: str
    password: str
    uuid_departament: str