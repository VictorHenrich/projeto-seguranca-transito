from .base_exception import BaseExceptionApplication


class AuthorizationNotFoundHeader(BaseExceptionApplication):
    def __init__(self) -> None:
        super().__init__(
            "Campo 'Authorization' não foi localizado ou definido incorretamente!"
        )
