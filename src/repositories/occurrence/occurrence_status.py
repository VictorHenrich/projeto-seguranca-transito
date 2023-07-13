from enum import Enum


class OccurrenceStatus(Enum):
    PROGRESS: str = "ANDAMENTO"
    PROCESS: str = "PROCESSO"
    ERROR: str = "FALHA"
    SUCCESS: str = "SUCESSO"
