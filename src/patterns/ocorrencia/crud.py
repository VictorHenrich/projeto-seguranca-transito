from dataclasses import dataclass
from abc import ABC



@dataclass
class OccurrenceData(ABC):
    descricao: str
    obs: str
    status: str


@dataclass
class OccurrenceRegistration(OccurrenceData):
    uuid_usuario: str
    status: str = "pendente"
    


@dataclass
class OccurrenceView(OccurrenceData):
    uuid: str