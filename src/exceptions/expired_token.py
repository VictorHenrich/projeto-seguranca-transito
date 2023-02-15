class ExpiredTokenError(Exception):
    def __init__(self) -> None:
        super().__init__("Token expirado!")
