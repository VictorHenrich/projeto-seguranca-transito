from dataclasses import dataclass

from start import app
from patterns.repository import IFindRepository
from models import Departamento
from repositories.departament import (
    DepartamentFindRepository,
    DepartamentFindRepositoryParams,
)


@dataclass
class DepartamentFindProps:
    departament_id: str


class DepartamentGettingService:
    def execute(self, departament_id: int) -> Departamento:
        with app.databases.create_session() as session:
            getting_repository_param: DepartamentFindRepositoryParams = (
                DepartamentFindProps(departament_id)
            )

            getting_repository: IFindRepository[
                DepartamentFindRepositoryParams, Departamento
            ] = DepartamentFindRepository(session)

            departament: Departamento = getting_repository.get(getting_repository_param)

            return departament
