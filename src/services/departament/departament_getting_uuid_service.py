from dataclasses import dataclass

from start import app
from patterns.repository import IFindRepository
from models import Departament
from repositories.departament import (
    DepartamentFindUUIDRepository,
    DepartamentFindUUIDRepositoryParams,
)


@dataclass
class DepartamentFindUUIDProps:
    uuid_departament: str


class DepartamentGettingUUIDService:
    def execute(self, uuid_departament: str) -> Departament:
        with app.databases.create_session() as session:
            getting_repository_param: DepartamentFindUUIDRepositoryParams = (
                DepartamentFindUUIDProps(uuid_departament=uuid_departament)
            )

            getting_repository: IFindRepository[
                DepartamentFindUUIDRepositoryParams, Departament
            ] = DepartamentFindUUIDRepository(session)

            departament: Departament = getting_repository.get(getting_repository_param)

            return departament
