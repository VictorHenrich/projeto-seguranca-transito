from dataclasses import dataclass

from server import App
from patterns.repository import IFindRepository
from models import Departament
from repositories.departament import (
    DepartamentFindRepository,
    DepartamentFindRepositoryParams,
)


@dataclass
class DepartamentFindingServiceProps:
    departament_id: int


class DepartamentFindingService:
    def execute(self, props: DepartamentFindingServiceProps) -> Departament:
        with App.databases.create_session() as session:
            getting_repository: IFindRepository[
                DepartamentFindRepositoryParams, Departament
            ] = DepartamentFindRepository(session)

            departament: Departament = getting_repository.find_one(props)

            return departament
