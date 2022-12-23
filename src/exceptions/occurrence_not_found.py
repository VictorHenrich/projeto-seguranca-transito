

class OccurrenceNotFoundError(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__('Ocorrência não localizada!')