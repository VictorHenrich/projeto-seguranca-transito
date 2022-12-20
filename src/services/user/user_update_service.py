import re
from datetime import date

from start import app
from server.database import Database
from patterns.service import IService
from patterns.repository import IUpdateRepository
from repositories.user import (
    UserUpdateRepository,
    UserUpdateRepositoryParam
)


class UserUpdateService(IService[None]):
    def __handle_repository_param(
        self,
        uuid_user: str,
        name: str,
        email: str,
        password: str,
        document: str,
        birthday: str,
        status: bool = False
    ) -> UserUpdateRepositoryParam:
        name: str = name.upper()

        email: str = email.upper()

        document: str = re.sub(r"[^0-9]", document)

        password: str = password

        birth: date = date(*(birthday.split("-")))
        
        return UserUpdateRepositoryParam(
            name=name,
            email=email,
            document=document,
            password=password,
            birthday=birth,
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