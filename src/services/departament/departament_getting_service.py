from dataclasses import dataclass

from server import App
from patterns.repository import IFindRepository
from models import Departament
from repositories.departament import (
    DepartamentFindRepository,
    DepartamentFindRepositoryParams,
)


@dataclass
class DepartamentGettingServiceProps:
    departament_id: int


class DepartamentGettingService:
    def execute(self, props: DepartamentGettingServiceProps) -> Departament:
        with App.databases().create_session() as session:
            getting_repository: IFindRepository[
                DepartamentFindRepositoryParams, Departament
            ] = DepartamentFindRepository(session)

            departament: Departament = getting_repository.get(props)

            return departament
