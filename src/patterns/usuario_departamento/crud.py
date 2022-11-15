from abc import ABC
from dataclasses import dataclass


@dataclass
class DepartamentUserData(ABC):
    nome: str


@dataclass
class DepartamentUserRegistration(DepartamentUserData):
    usuario: str
    senha: str
    cargo: str


@dataclass
class DepartamentUserView(DepartamentUserData):
    cargo: str
    uuid: str