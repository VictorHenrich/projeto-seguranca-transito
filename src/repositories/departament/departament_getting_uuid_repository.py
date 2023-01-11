from dataclasses import dataclass

from patterns.repository import BaseRepository
from models import Departamento
from exceptions import DepartamentNotFoundError



@dataclass
class DepartamentGettingUUIDRepositoryParam:
    uuid_departament: str



class DepartamentGettingUUIDRepository(BaseRepository):
    def get(self, param: DepartamentGettingUUIDRepositoryParam) -> Departamento:
        departament: Departamento = \
            self.session\
                    .query(Departamento)\
                    .filter(Departamento.id_uuid == param.uuid_departament)\
                    .first()

        if not departament:
            raise DepartamentNotFoundError()

        return departament