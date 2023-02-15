from start import app
from patterns.repository import IExclusionRepository
from repositories.user import UserExclusionRepositoryParam, UserExclusionRepository


class UserExclusionService:
    def __handle_repository_param(self, uuid_user: str) -> UserExclusionRepositoryParam:
        return UserExclusionRepositoryParam(uuid_ser=uuid_user)

    def execute(self, uuid_user: str) -> None:
        with app.databases.create_session() as session:
            repository: IExclusionRepository[
                UserExclusionRepositoryParam
            ] = UserExclusionRepository(session)

            repository_param: UserExclusionRepositoryParam = (
                self.__handle_repository_param(uuid_user)
            )

            repository.delete(repository_param)

            session.commit()
