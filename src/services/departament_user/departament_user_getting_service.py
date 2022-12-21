from start import app
from server.database import Database
from patterns.repository import IGettingRepository
from repositories.departament_user import (
    DepartamentUserGettingRepository,
    DepartamentUserGettingRepositoryParam
)
from models import UsuarioDepartamento, Departamento



class DepartamentUserGettingService:
    def execute(
        self,
        departament: Departamento,
        uuid_departament_user: UsuarioDepartamento
    ) -> UsuarioDepartamento:
        database: Database = app.databases.get_database()

        getting_repository_param: DepartamentUserGettingRepositoryParam = \
            DepartamentUserGettingRepositoryParam(
                departament=departament,
                uuid_departament_user=uuid_departament_user
            )

        getting_repository: IGettingRepository[DepartamentUserGettingRepositoryParam, UsuarioDepartamento] = \
            DepartamentUserGettingRepository(database)

        user: UsuarioDepartamento = getting_repository.get(getting_repository_param)

        return user