from dataclasses import dataclass

from start import app
from patterns.repository import IFindRepository
from repositories.user import UserFindRepository, UserFindRepositoryParams
from models import Usuario


@dataclass
class UserFindProps:
    uuid_user: str


class UserGettingService:
    def __handle_repository_param(self, uuid_user: str) -> UserFindRepositoryParams:
        return UserFindRepositoryParams(uuid_user)

    def execute(self, uuid_user: str) -> Usuario:
        with app.databases.create_session() as session:
            repository_param: UserFindRepositoryParams = UserFindProps(uuid_user)

            repository: IFindRepository[
                UserFindRepositoryParams, Usuario
            ] = UserFindRepository(session)

            user: Usuario = repository.get(repository_param)

            return user
