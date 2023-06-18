from typing import Collection, Tuple, TypeAlias
from dataclasses import dataclass
from sqlalchemy.orm import Session


from server import App
from patterns.repository import IAggregateRepository
from repositories.user import UserAggregateRepository, UserAggregateRepositoryParams
from models import User, Vehicle, Occurrence


UserLoaded: TypeAlias = Tuple[User, Collection[Vehicle], Collection[Occurrence]]


@dataclass
class UserFindProps:
    user_uuid: str


class UserLoadService:
    def __init__(self, user_uuid: str) -> None:
        self.__user_props: UserFindProps = UserFindProps(user_uuid)

    def __find_user(self, session: Session) -> UserLoaded:
        user_aggregate_repository: IAggregateRepository[
            UserAggregateRepositoryParams, UserLoaded
        ] = UserAggregateRepository(session)

        return user_aggregate_repository.aggregate(self.__user_props)

    def execute(self) -> UserLoaded:
        with App.databases.create_session() as session:
            return self.__find_user(session)
