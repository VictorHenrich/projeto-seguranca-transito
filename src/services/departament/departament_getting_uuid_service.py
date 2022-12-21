from start import app
from server.database import Database
from patterns.repository import IGettingRepository
from models import Departamento
from repositories.departament import (
    DepartamentGettingUUIDRepository,
    DepartamentGettingUUIDRepositoryParam
)


class DepartamentGettingUUIDService:
    def execute(
        self,
        uuid_departament: str
    ) -> Departamento:
        database: Database = app.databases.get_database()

        getting_repository_param: DepartamentGettingUUIDRepositoryParam = \
            DepartamentGettingUUIDRepositoryParam(
                uuid_departament=uuid_departament
            )

        getting_repository: IGettingRepository[DepartamentGettingUUIDRepositoryParam, Departamento] = \
            DepartamentGettingUUIDRepository(database)

        departament: Departamento = getting_repository.get(getting_repository_param)

        return departament