from dataclasses import dataclass

from patterns.repository import BaseRepository
from models import Departamento
from exceptions import DepartamentNotFoundError



@dataclass
class DepartamentGettingRepositoryParam:
    departament_id: str



class DepartamentGettingRepository(BaseRepository):
    def get(self, param: DepartamentGettingRepositoryParam) -> Departamento:
        departament: Departamento = \
            self.session\
                    .query(Departamento)\
                    .filter(Departamento.id == param.departament_id)\
                    .first()

        if not departament:
            raise DepartamentNotFoundError()

        return departament