class TokenTypeNotBearerError(Exception):
    def __init__(self) -> None:
        super().__init__("Tipo de token não é Bearer!")
