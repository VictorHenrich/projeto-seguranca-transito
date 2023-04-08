from dataclasses import dataclass

from server import App
from patterns.repository import IFindRepository
from models import Departament
from repositories.departament import (
    DepartamentFindUUIDRepository,
    DepartamentFindUUIDRepositoryParams,
)


@dataclass
class DepartamentFindingUUIDServiceProps:
    departament_uuid: str


class DepartamentFindingUUIDService:
    def execute(self, props: DepartamentFindingUUIDServiceProps) -> Departament:
        with App.databases.create_session() as session:
            getting_repository: IFindRepository[
                DepartamentFindUUIDRepositoryParams, Departament
            ] = DepartamentFindUUIDRepository(session)

            departament: Departament = getting_repository.find_one(props)

            return departament
