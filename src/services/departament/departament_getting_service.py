from start import app
from server.database import Database
from patterns.repository import IGettingRepository
from models import Departamento
from repositories.departament import (
    DepartamentGettingRepository,
    DepartamentGettingRepositoryParam
)


class DepartamentGettingService:
    def execute(
        self,
        departament_id: int
    ) -> Departamento:
        database: Database = app.databases.get_database()

        getting_repository_param: DepartamentGettingRepositoryParam = \
            DepartamentGettingRepositoryParam(departament_id)

        getting_repository: IGettingRepository[DepartamentGettingRepositoryParam, Departamento] = \
            DepartamentGettingRepository(database)

        departament: Departamento = getting_repository.get(getting_repository_param)

        return departament