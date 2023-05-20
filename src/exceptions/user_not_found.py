from .base_exception import BaseExceptionApplication

class UserNotFoundError(BaseExceptionApplication):
    def __init__(self) -> None:
        super().__init__("Usuário não localizado!")
