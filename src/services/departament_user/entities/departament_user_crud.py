from dataclasses import dataclass
from typing import Optional
from models import Departamento



@dataclass
class DepartamentUserRegistration:
    name: str
    user: str
    password: str
    office: str
    departament: Optional[Departamento] = None



@dataclass
class DepartamentUserLocation:
    uuid: str
    departament: Departamento 


@dataclass
class DepartamentUserUpgrade:
    data: DepartamentUserRegistration
    location_data: DepartamentUserLocation
