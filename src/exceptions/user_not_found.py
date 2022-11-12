


class UserNotFoundError(Exception):
    def __init__(self) -> None:
        super().__init__("Usuário não localizado!")