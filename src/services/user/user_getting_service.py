from start import app
from server.database import Database
from patterns.repository import IGettingRepository
from repositories.user import (
    UserGettingRepository,
    UserGettingRepositoryParam
)
from models import Usuario



class UserGettingService:
    def __handle_repository_param(self, uuid_user: str) -> UserGettingRepositoryParam:
        return UserGettingRepositoryParam(
            uuid_user
        )

    def execute(self, uuid_user: str) -> Usuario:
        database: Database = app.databases.get_database()

        repository_param: UserGettingRepositoryParam = \
            self.__handle_repository_param(uuid_user)

        repository: IGettingRepository[UserGettingRepositoryParam, Usuario] = UserGettingRepository(database)

        user: Usuario = repository.load(repository_param)

        return user