from .base_exception import BaseExceptionApplication


class DatabaseNotFoundError(BaseExceptionApplication):
    def __init__(self, empty: bool = False) -> None:
        error_message = (
            "Nenhum banco de dados foi localizado!"
            if not empty
            else "Não existe nenhum instancia de banco!"
        )

        super().__init__(error_message)
