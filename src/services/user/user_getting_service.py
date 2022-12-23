from start import app
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
        with app.databases.create_session() as session:
            repository_param: UserGettingRepositoryParam = \
                self.__handle_repository_param(uuid_user)

            repository: IGettingRepository[UserGettingRepositoryParam, Usuario] = \
                UserGettingRepository(session)

            user: Usuario = repository.get(repository_param)

            return user