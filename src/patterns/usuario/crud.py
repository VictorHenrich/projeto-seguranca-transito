from typing import Optional
from abc import ABC



class UserData(ABC):
    def __init__(
        self,
        nome: str,
        email: str,
        cpf: str,
        data_nascimento: Optional[str] = None
    ) -> None:
        self.nome: str = nome
        self.email: str = email
        self.cpf: str = cpf
        self.data_nascimento: Optional[str] = data_nascimento



class UserRegistration(UserData):
    def __init__(
        self, 
        nome: str, 
        email: str, 
        cpf: str,
        senha: str,
        data_nascimento: Optional[str] = None
    ) -> None:
        super().__init__(nome, email, cpf, data_nascimento)

        self.senha: str = senha



class UserView(UserData):
    def __init__(
        self, 
        nome: str, 
        email: str, 
        cpf: str,
        data_cadastro: str,
        uuid: str,
        data_nascimento: Optional[str] = None
    ) -> None:
        super().__init__(nome, email, cpf, data_nascimento)

        self.data_cadastro: str = data_cadastro
        self.uuid: str = uuid






