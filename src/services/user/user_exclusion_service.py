from start import app
from server.database import Database
from patterns.repository import IExclusionRepository
from repositories.user import (
    UserExclusionRepositoryParam,
    UserExclusionRepository
)




class UserExclusionService:
    def __handle_repository_param(self, uuid_user: str) -> UserExclusionRepositoryParam:
        return UserExclusionRepositoryParam(
            uuid_ser=uuid_user
        )

    def execute(self, uuid_user: str) -> None:
        database: Database = app.databases.get_database()

        repository: IExclusionRepository[UserExclusionRepositoryParam] = UserExclusionRepository(database)

        repository_param: UserExclusionRepositoryParam = self.__handle_repository_param(uuid_user)

        repository.delete(repository_param)