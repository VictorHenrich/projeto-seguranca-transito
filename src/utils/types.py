from enum import Enum


class VehicleTypes(Enum):
    CAR = "CARRO"
    MOTOR = "MOTOR"


class OccurrenceStatus(Enum):
    PROGRESS = "ANDAMENTO"
    PROCESS = "PROCESSO"
    ERROR = "FALHA"
    SUCCESS = "SUCESSO"
