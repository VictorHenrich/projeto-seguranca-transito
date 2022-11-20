

class OccurrenceTypeNotFoundError(Exception):
    def __init__(self) -> None:
        super().__init__('Tipo de Ocorrência não localizada!')