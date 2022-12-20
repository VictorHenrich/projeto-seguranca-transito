from start import app
from server.database import Database
from patterns.repository import IAuthRepository
from patterns.service import IService
from repositories.user import (
    UserAuthRepository,
    UserAuthRepositoryParam
)
from models import Usuario




class UserAuthenticationService(IService[Usuario]):
    def __handle_repository_param(
        self,
        email: str,
        password: str
    ) -> UserAuthRepositoryParam:
        return UserAuthRepositoryParam(
            email,
            password
        )

    def execute(
        self,
        email: str,
        password: str
    ) -> Usuario:
        database: Database = app.databases.get_database()

        repository: IAuthRepository[UserAuthRepositoryParam, Usuario] = UserAuthRepository(database)

        repository_param: UserAuthRepositoryParam = \
            self.__handle_repository_param(
                email,
                password
            )

        user: Usuario = repository.auth(repository_param)

        return user