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
    def execute(self, props: UserCreationServiceProps) -> None:
        with App.databases.create_session() as session:
            repository: ICreateRepository[
                UserCreateRepositoryParams, None
            ] = UserCreateRepository(session)

            repository.create(props)

            session.commit()
