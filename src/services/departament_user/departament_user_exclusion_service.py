from start import app
from server.database import Database
from patterns.repository import IExclusionRepository
from repositories.departament_user import (
    DepartamentUserExclusionRepository,
    DepartamentUserExclusionRepositoryParam
)
from models import UsuarioDepartamento, Departamento


class DepartamentUserExclusionService:
    def execute(
        self,
        departament: Departamento,
        uuid_departament_user: UsuarioDepartamento
    ) -> None:
        database: Database = app.databases.get_database()

        exclusion_repository_param: DepartamentUserExclusionRepositoryParam = \
            DepartamentUserExclusionRepositoryParam(
                departament=departament,
                uuid_departament_user=uuid_departament_user
            )

        exclusion_repository: IExclusionRepository[DepartamentUserExclusionRepositoryParam] = \
            DepartamentUserExclusionRepository(database)

        exclusion_repository.delete(exclusion_repository_param)