from typing import Optional
import re
from datetime import date

from start import app
from server.database import Database
from patterns.repository import IUpdateRepository
from repositories.user import (
    UserUpdateRepository,
    UserUpdateRepositoryParam
)


class UserUpdateService:
    def __handle_repository_param(
        self,
        uuid_user: str,
        name: str,
        email: str,
        password: str,
        document: str,
        birthday: Optional[str],
        status: bool = False
    ) -> UserUpdateRepositoryParam:
        treaty_name: str = name.upper()

        treaty_email: str = email.upper()

        treaty_document: str = re.sub(r"[^0-9]", '', document)

        traety_password: str = password.strip()

        treaty_birthday: Optional[date] = date(*(birthday.split("-"))) if birthday and len(birthday) else None
        
        return UserUpdateRepositoryParam(
            name=treaty_name,
            email=treaty_email,
            document=treaty_document,
            password=traety_password,
            birthday=treaty_birthday,
            uuid_user=uuid_user,
            status=status
        )

    def execute(
        self,
        uuid_user: str,
        name: str,
        email: str,
        password: str,
        document: str,
        birthday: str,
        status: bool = False
    ) -> None:
        database: Database = app.databases.get_database()

        repository_param: UserUpdateRepositoryParam = \
            self.__handle_repository_param(
                uuid_user=uuid_user,
                name=name,
                email=email,
                password=password,
                document=document,
                birthday=birthday,
                status=status
            )

        repository: IUpdateRepository[UserUpdateRepositoryParam] = UserUpdateRepository(database)

        repository.update(repository_param)