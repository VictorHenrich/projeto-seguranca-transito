from dataclasses import dataclass

from start import app
from patterns.repository import IDeleteRepository
from repositories.user import UserDeleteRepository, UserDeleteRepositoryParams


@dataclass
class UserDeleteProps:
    uuid_ser: str


class UserExclusionService:
    def __handle_repository_param(self, uuid_user: str) -> UserDeleteRepositoryParams:
        return UserDeleteRepositoryParams(uuid_ser=uuid_user)

    def execute(self, uuid_user: str) -> None:
        with app.databases.create_session() as session:
            repository: IDeleteRepository[
                UserDeleteRepositoryParams
            ] = UserDeleteRepository(session)

            repository_param: UserDeleteRepositoryParams = (
                self.__handle_repository_param(uuid_user)
            )

            repository.delete(repository_param)

            session.commit()
