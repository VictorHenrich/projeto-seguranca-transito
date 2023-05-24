class MiddlewareErrorValue(ValueError):
    def __init__(
        self,
    ) -> None:
        message: str = "Valor passado como parametro ao middleware está inválido!"

        super().__init__(message)
