from dataclasses import dataclass
from abc import ABC



@dataclass
class CRUDOccurrenceData(ABC):
    descricao: str
    obs: str
    status: str


@dataclass
class CRUDOccurrenceRegistration(CRUDOccurrenceData):
    uuid_usuario: str
    status: str = "pendente"
    


@dataclass
class CRUDOccurrenceView(CRUDOccurrenceData):
    uuid: str