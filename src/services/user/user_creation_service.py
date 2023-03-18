from typing import Optional
from datetime import date
import re
from dataclasses import dataclass

from start import app
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
        with app.databases.create_session() as session:
            repository: ICreateRepository[
                UserCreateRepositoryParams, None
            ] = UserCreateRepository(session)

            repository.create(props)

            session.commit()
