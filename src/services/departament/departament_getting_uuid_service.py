from dataclasses import dataclass

from server import App
from patterns.repository import IFindRepository
from models import Departament
from repositories.departament import (
    DepartamentFindUUIDRepository,
    DepartamentFindUUIDRepositoryParams,
)


@dataclass
class DepartamentGettingUUIDServiceProps:
    uuid_departament: str


class DepartamentGettingUUIDService:
    def execute(self, props: DepartamentGettingUUIDServiceProps) -> Departament:
        with App.databases.create_session() as session:
            getting_repository: IFindRepository[
                DepartamentFindUUIDRepositoryParams, Departament
            ] = DepartamentFindUUIDRepository(session)

            departament: Departament = getting_repository.get(props)

            return departament
