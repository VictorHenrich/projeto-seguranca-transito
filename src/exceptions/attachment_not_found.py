from .base_exception import BaseExceptionApplication


class AttachmentNotFoundError(BaseExceptionApplication):
    def __init__(self) -> None:
        super().__init__("O arquivo não foi encontrado!")
