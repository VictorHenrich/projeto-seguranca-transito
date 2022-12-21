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
        date_birth: str
    ) -> UserCreationRepositoryParam:

        name: str = name.upper()

        email: str = email.upper()

        document: str = re.sub(r"[^0-9]", document)

        password: str = password

        birth: date = date(*(date_birth.split("-")))
        
        return UserCreationRepositoryParam(
            name=name,
            email=email,
            document=document,
            password=password,
            birthday=birth
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
                date_birth=birthday
            )

        repository: ICreationRepository[UserCreationRepositoryParam] = UserCreationRepository(database)

        repository.create(repository_param)