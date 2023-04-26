from typing import Optional
from datetime import date
from dataclasses import dataclass

from server import App
from patterns.repository import ICreateRepository
from repositories.user import UserCreateRepository, UserCreateRepositoryParams


@dataclass
class UserCreationServiceProps:
    name: str
    email: str
    password: str
    document: str
    birthday: Optional[date]


class UserCreationService:
    def __init__(
        self,
        name: str,
        email: str,
        password: str,
        document: str,
        birthday: Optional[date],
    ):
        self.__props: UserCreationServiceProps = UserCreationServiceProps(
            name, email, password, document, birthday
        )

    def execute(self) -> None:
        with App.databases.create_session() as session:
            repository: ICreateRepository[
                UserCreateRepositoryParams, None
            ] = UserCreateRepository(session)

            repository.create(self.__props)

            session.commit()
