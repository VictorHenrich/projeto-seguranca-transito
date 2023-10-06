from .base_exception import BaseExceptionApplication


class InvalidUserPasswordError(BaseExceptionApplication):
    def __init__(self, user_uuid: str) -> None:
        super().__init__(f"Senha passada do usuário {user_uuid} é inválida!")
