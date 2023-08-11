from dataclasses import dataclass
from datetime import date

from server import Databases
from models import User
from patterns.repository import IUpdateRepository
from repositories.user import (
    UserFindAndUpdateRepository,
    UserFindAndUpdateRepositoryParams,
)


@dataclass
class UserUpdateProps:
    user_uuid: str
    name: str
    email: str
    password: str
    document: str
    document_rg: str
    telephone: str
    state_issuer: str
    address_state: str
    address_city: str
    address_district: str
    address_street: str
    address_number: str
    birthday: date


class UserUpdateService:
    def __init__(
        self,
        user_uuid: str,
        name: str,
        email: str,
        password: str,
        document: str,
        document_rg: str,
        telephone: str,
        state_issuer: str,
        address_state: str,
        address_city: str,
        address_district: str,
        address_street: str,
        address_number: str,
        birthday: date,
    ) -> None:
        self.__props: UserUpdateProps = UserUpdateProps(
            user_uuid,
            name,
            email,
            password,
            document,
            document_rg,
            telephone,
            state_issuer,
            address_state,
            address_city,
            address_district,
            address_street,
            address_number,
            birthday,
        )

    def execute(self) -> None:
        with Databases.create_session() as session:
            repository: IUpdateRepository[
                UserFindAndUpdateRepositoryParams, User
            ] = UserFindAndUpdateRepository(session)

            repository.update(self.__props)

            session.commit()
