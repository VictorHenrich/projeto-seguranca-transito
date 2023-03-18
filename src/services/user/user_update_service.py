from dataclasses import dataclass
from datetime import date

from start import app
from patterns.repository import IUpdateRepository
from repositories.user import UserUpdateRepository, UserUpdateRepositoryParam


@dataclass
class UserUpdateServiceProps:
    uuid_user: str
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
        with app.databases.create_session() as session:
            repository: IUpdateRepository[
                UserUpdateRepositoryParam, None
            ] = UserUpdateRepository(session)

            repository_params: UserUpdateParams = UserUpdateParams(
                uuid_user=props.uuid_user,
                name=props.name,
                email=props.email,
                password=props.password,
                document=props.document,
                birthday=date(0, 0, 0),
                status=props.status,
            )

            repository.update(repository_params)

            session.commit()
