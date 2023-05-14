from dataclasses import dataclass

from server import App
from patterns.repository import IDeleteRepository
from repositories.user import UserDeleteRepository, UserDeleteRepositoryParams


@dataclass
class UserDeleteProps:
    user_uuid: str


class UserExclusionService:
    def __init__(self, user_uuid: str) -> None:
        self.__props: UserDeleteProps = UserDeleteProps(user_uuid)

    def execute(self) -> None:
        with App.databases.create_session() as session:
            repository: IDeleteRepository[
                UserDeleteRepositoryParams, None
            ] = UserDeleteRepository(session)

            repository.delete(self.__props)

            session.commit()
