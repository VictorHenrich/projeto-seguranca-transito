from dataclasses import dataclass

from server import App
from patterns.repository import IFindRepository
from repositories.user import UserFindRepository, UserFindRepositoryParams
from models import User


@dataclass
class UserGettingServiceProps:
    uuid_user: str


class UserGettingService:
    def execute(self, props: UserGettingServiceProps) -> User:
        with App.databases().create_session() as session:
            repository: IFindRepository[
                UserFindRepositoryParams, User
            ] = UserFindRepository(session)

            user: User = repository.get(props)

            return user
