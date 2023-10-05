from dataclasses import dataclass
from datetime import date

from server import Databases
from models import User
from patterns.repository import IUpdateRepository
from repositories.user import (
    UserFindAndUpdateRepository,
    UserFindAndUpdateRepositoryParams,
)
from utils.entities import AddressPayload


@dataclass
class UserUpdateProps:
    user_uuid: str
    name: str
    email: str
    document: str
    document_rg: str
    telephone: str
    state_issuer: str
    address_state: str
    address_city: str
    address_district: str
    address_street: str
    address_number: str
    address_zipcode: str
    birthday: date


class UserUpdateService:
    def __init__(
        self,
        user_uuid: str,
        name: str,
        email: str,
        document: str,
        document_rg: str,
        telephone: str,
        state_issuer: str,
        address: AddressPayload,
        birthday: date,
    ) -> None:
        self.__props: UserUpdateProps = UserUpdateProps(
            user_uuid,
            name,
            email,
            document,
            document_rg,
            telephone,
            state_issuer,
            address.state,
            address.city,
            address.district,
            address.street,
            address.number,
            address.zipcode,
            birthday,
        )

    def execute(self) -> None:
        with Databases.create_session() as session:
            repository: IUpdateRepository[
                UserFindAndUpdateRepositoryParams, User
            ] = UserFindAndUpdateRepository(session)

            repository.update(self.__props)

            session.commit()
