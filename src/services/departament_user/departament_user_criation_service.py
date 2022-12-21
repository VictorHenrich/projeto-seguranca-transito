from start import app
from server.database import Database
from patterns.repository import ICreationRepository
from models import Departamento
from repositories.departament_user import (
    DepartamentUserCreationRepository,
    DepartamentUserCreationRepositoryParam
)


class DepartamentUserCriationService:
    def execute(
        self,
        departament: Departamento,
        name: str,
        user: str,
        password: str,
        position: str
    ) -> None:
        database: Database = app.databases.get_database()

        creating_repository_param: DepartamentUserCreationRepositoryParam = \
            DepartamentUserCreationRepositoryParam(
                departament=departament,
                name=name,
                access=user,
                password=password,
                position=position
            )

        creating_repository: ICreationRepository[DepartamentUserCreationRepositoryParam] = \
            DepartamentUserCreationRepository(database)

        creating_repository.create(creating_repository_param)