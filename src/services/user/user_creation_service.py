from typing import Optional
from datetime import date
import re

from start import app
from server.database import Database
from patterns.repository import ICreationRepository
from repositories.user import (
    UserCreationRepository,
    UserCreationRepositoryParam
)


class UserCreationService:
    def __handle_params_repository(
        self,
        name: str,
        email: str,
        document: str,
        password: str,
        birthday: Optional[str]
    ) -> UserCreationRepositoryParam:

        treaty_name: str = name.upper()

        treaty_email: str = email.upper()

        treaty_document: str = re.sub(r"[^0-9]", '', document)

        traety_password: str = password.strip()

        treaty_birthday: Optional[date] = date(*(birthday.split("-"))) if birthday and len(birthday) else None
        
        return UserCreationRepositoryParam(
            name=treaty_name,
            email=treaty_email,
            document=treaty_document,
            password=traety_password,
            birthday=treaty_birthday
        )

    def execute(
        self,
        name: str,
        email: str,
        document: str,
        password: str,
        birthday: str
    ) -> None:
        database: Database = app.databases.get_database()

        repository_param: UserCreationRepositoryParam = \
            self.__handle_params_repository(
                name=name,
                email=email,
                document=document,
                password=password,
                birthday=birthday
            )

        repository: ICreationRepository[UserCreationRepositoryParam] = UserCreationRepository(database)

        repository.create(repository_param)