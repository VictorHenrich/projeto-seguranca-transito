class OccurrenceNotFoundError(Exception):
    def __init__(self) -> None:
        super().__init__('Ocorrencia não localizada!')