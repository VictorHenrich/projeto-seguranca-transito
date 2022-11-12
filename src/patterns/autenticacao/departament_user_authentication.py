from dataclasses import dataclass


@dataclass
class DepartamentUserAuthentication:
    departamento: str
    usuario: str
    senha: str