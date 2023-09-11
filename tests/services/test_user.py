from unittest import TestCase
from unittest.mock import Mock
from datetime import datetime

from src.models import User
from src.patterns.service import IService
from src.services.user import (
    UserCreationService,
    UserUpdateService,
    UserExclusionService,
)
from src.utils.entities import AddressPayload, VehiclePayload
from src.utils.types import VehicleTypes


class UserServiceCase(TestCase):
    def setUp(self) -> None:
        self.__user_payload: Mock = Mock()

        self.__user_payload.name = "Stephanie Machado"
        self.__user_payload.email = "stephaniemachadow@gmail.com"
        self.__user_payload.password = "1234"
        self.__user_payload.document = "222222222222"
        self.__user_payload.document_rg = "2222222"
        self.__user_payload.birthday = datetime(1998, 5, 27)
        self.__user_payload.address = AddressPayload(
            zipcode="0000",
            state="sc",
            city="capivari de baixo",
            district="caçador",
            street="rua antonio manuel dos santos",
            number="0",
        )
        self.__user_payload.state_issuer = "santa catarina"
        self.__user_payload.telephone = "48999197582"
        self.__user_payload.id_uuid = None

    def test_creation(self) -> None:
        self.__user_payload.vehicles = [
            VehiclePayload(
                plate="XYZ9999",
                renavam="12345678901",
                vehicle_type=VehicleTypes("CARRO"),
            ),
            VehiclePayload(
                plate="VHK88898",
                renavam="1000999200010",
                vehicle_type=VehicleTypes("MOTO"),
            ),
        ]

        user_creation_service: IService[User] = UserCreationService(
            name=self.__user_payload.name,
            email=self.__user_payload.email,
            password=self.__user_payload.password,
            document=self.__user_payload.document,
            birthday=self.__user_payload.birthday,
            document_rg=self.__user_payload.document_rg,
            state_issuer=self.__user_payload.state_issuer,
            telephone=self.__user_payload.telephone,
            address=self.__user_payload.address,
            vehicles=self.__user_payload.vehicles,
        )

        user_creation_service.execute()

    def test_update(self) -> None:
        self.__user_payload.id_uuid = "72b5a0ba-e454-4668-8965-f4901353c4e4"

        update_service: IService[None] = UserUpdateService(
            user_uuid=self.__user_payload.id_uuid,
            name=self.__user_payload.name,
            email=self.__user_payload.email,
            password=self.__user_payload.password,
            document=self.__user_payload.document,
            birthday=self.__user_payload.birthday,
            document_rg=self.__user_payload.document_rg,
            state_issuer=self.__user_payload.state_issuer,
            telephone=self.__user_payload.telephone,
            address=self.__user_payload.address,
        )

        update_service.execute()

    def test_exclusion(self) -> None:
        self.__user_payload.id_uuid = "ebd913c9-cd40-4822-af1f-822732cff2c4"

        exclusion_service: IService[None] = UserExclusionService(
            user_uuid=self.__user_payload.id_uuid
        )

        exclusion_service.execute()
