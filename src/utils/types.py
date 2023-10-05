from typing import TypeAlias, Mapping, Any
from enum import Enum


DictType: TypeAlias = Mapping[str, Any]


class VehicleTypes(Enum):
    CAR = "CARRO"
    MOTOR = "MOTO"


class OccurrenceStatus(Enum):
    PROGRESS = "ANDAMENTO"
    PROCESS = "PROCESSO"
    ERROR = "FALHA"
    SUCCESS = "SUCESSO"
