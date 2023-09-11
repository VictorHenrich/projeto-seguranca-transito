from enum import Enum


class VehicleTypes(Enum):
    CAR = "CARRO"
    MOTOR = "MOTO"


class OccurrenceStatus(Enum):
    PROGRESS = "ANDAMENTO"
    PROCESS = "PROCESSO"
    ERROR = "FALHA"
    SUCCESS = "SUCESSO"
