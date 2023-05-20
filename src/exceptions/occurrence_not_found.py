from .base_exception import BaseExceptionApplication

class OccurrenceNotFoundError(BaseExceptionApplication):
    def __init__(self) -> None:
        super().__init__("Ocorrência não localizada!")
