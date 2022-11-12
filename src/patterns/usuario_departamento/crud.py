from abc import ABC



class DepartamentUserData(ABC):
    def __init__(
        self,
        nome: str
    ) -> None:
        self.nome: str = nome



class DepartamentUserRegistration(DepartamentUserData):
    def __init__(self, nome: str, usuario: str, senha: str, cargo: str) -> None:
        super().__init__(nome)

        self.usuario: str = usuario

        self.senha: str = senha

        self.cargo: str = cargo


class DepartamentUserView(DepartamentUserData):
    def __init__(self, nome: str) -> None:
        super().__init__(nome)