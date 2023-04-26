from typing import Optional
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
    birthday: date
    status: bool


class UserUpdateService:
    def __init__(
        self,
        user_uuid: str,
        name: str,
        email: str,
        password: str,
        document: str,
        birthday: date,
        status: bool,
    ) -> None:
        self.__props: UserUpdateServiceProps = UserUpdateServiceProps(
            user_uuid,
            name,
            email,
            password,
            document,
            birthday,
            status,
        )

    def execute(self) -> None:
        with App.databases.create_session() as session:
            repository: IUpdateRepository[
                UserUpdateRepositoryParams, None
            ] = UserUpdateRepository(session)

            repository.update(self.__props)

            session.commit()
