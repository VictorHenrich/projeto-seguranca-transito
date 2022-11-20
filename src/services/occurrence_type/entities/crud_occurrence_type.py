from dataclasses import dataclass
from models import Nivel, Departamento


@dataclass
class OccurrenceTypeRegistration:
    description: str
    instruction: str
    level: Nivel


@dataclass
class OccurrenceTypeLocation:
    uuid: str


@dataclass
class OccurrenceTypeUpgrade:
    data: OccurrenceTypeRegistration
    location_data: OccurrenceTypeLocation


@dataclass
class OccurrenceTypeListingLocation:
    departament: Departamento