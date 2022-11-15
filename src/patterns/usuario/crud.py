from typing import Optional
from dataclasses import dataclass
from abc import ABC


@dataclass
class UserData(ABC):
    nome: str
    email: str
    cpf: str
    data_nascimento: Optional[str]


@dataclass
class UserRegistration(UserData):
    senha: str
    data_nascimento: Optional[str] = None


@dataclass
class UserView(UserData):
    data_cadastro: str
    uuid: str
    data_nascimento: Optional[str] = None






