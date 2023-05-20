from .base_exception import BaseExceptionApplication


class DatabaseNotFoundError(BaseExceptionApplication):
    def __init__(self) -> None:
        super().__init__("Nenhum banco de dados foi localizado!")
