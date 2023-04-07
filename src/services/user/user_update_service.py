from dataclasses import dataclass
from datetime import date

from server import App
from patterns.repository import IUpdateRepository
from repositories.user import UserUpdateRepository, UserUpdateRepositoryParams


@dataclass
class UserUpdateServiceProps:
    user_uuid: str
    name: str
    email: str
    password: str
    document: str
    birthday: str
    status: bool = False


@dataclass
class UserUpdateParams(UserUpdateServiceProps):
    birthday: date


class UserUpdateService:
    def execute(self, props: UserUpdateServiceProps) -> None:
        with App.databases.create_session() as session:
            repository: IUpdateRepository[
                UserUpdateRepositoryParams, None
            ] = UserUpdateRepository(session)

            repository_params: UserUpdateParams = UserUpdateParams(
                user_uuid=props.user_uuid,
                name=props.name,
                email=props.email,
                password=props.password,
                document=props.document,
                birthday=date(0, 0, 0),
                status=props.status,
            )

            repository.update(repository_params)

            session.commit()
