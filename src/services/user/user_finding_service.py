from dataclasses import dataclass

from server import App
from patterns.repository import IFindRepository
from repositories.user import UserFindRepository, UserFindRepositoryParams
from models import User


@dataclass
class UserFindProps:
    user_uuid: str


class UserFindingService:
    def __init__(self, user_uuid: str) -> None:
        self.__props: UserFindProps = UserFindProps(user_uuid)

    def execute(self) -> User:
        with App.databases.create_session() as session:
            repository: IFindRepository[
                UserFindRepositoryParams, User
            ] = UserFindRepository(session)

            user: User = repository.find_one(self.__props)

            return user
