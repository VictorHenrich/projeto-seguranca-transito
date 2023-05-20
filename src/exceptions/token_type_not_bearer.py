from .base_exception import BaseExceptionApplication


class TokenTypeNotBearerError(BaseExceptionApplication):
    def __init__(self) -> None:
        super().__init__("Tipo de token não é Bearer!")
