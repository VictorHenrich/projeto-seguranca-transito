from unittest import TestCase
from unittest.mock import Mock, MagicMock
from datetime import datetime

from src.models import User
from src.patterns.service import IService
from src.services.user import (
    UserCreationService,
    UserUpdateService,
    UserAuthenticationService,
    UserExclusionService,
)


class UserServiceCase(TestCase):
    def setUp(self) -> None:
        self.__user_payload: Mock = Mock()

        self.__user_payload.name = "usuário alterado"
        self.__user_payload.email = "stephaniemachadow@gmail.com"
        self.__user_payload.password = "1234"
        self.__user_payload.document = "222222222222"
        self.__user_payload.document_rg = "2222222"
        self.__user_payload.birthday = datetime(1998, 5, 27)
        self.__user_payload.address_city = "capivari de baixo"
        self.__user_payload.address_district = "caçador"
        self.__user_payload.address_number = "0"
        self.__user_payload.address_state = "sc"
        self.__user_payload.address_street = "rua antonio manuel dos santos"
        self.__user_payload.state_issuer = "santa catarina"
        self.__user_payload.telephone = "48999197582"
        self.__user_payload.id_uuid = None

    def test_creation(self) -> None:
        vehicle_payload: MagicMock = MagicMock()

        vehicle_payload.__getitem__.side_effect = lambda key: {
            "plate": "XYZ9999",
            "renavam": "12345678901",
            "vehicle_type": "CARRO",
        }[key]

        vehicle_payload.get.side_effect = lambda key, default=None: {
            "brand": None,
            "chassi": None,
            "color": None,
            "model": None,
            "have_safe": False,
            "year": None,
        }.get(key, default)

        self.__user_payload.vehicles = [vehicle_payload]

        user_creation_service: IService[User] = UserCreationService(
            name=self.__user_payload.name,
            email=self.__user_payload.email,
            password=self.__user_payload.password,
            document=self.__user_payload.document,
            birthday=self.__user_payload.birthday,
            address_city=self.__user_payload.address_city,
            address_district=self.__user_payload.address_district,
            address_number=self.__user_payload.address_number,
            address_state=self.__user_payload.address_state,
            address_street=self.__user_payload.address_street,
            document_rg=self.__user_payload.document_rg,
            state_issuer=self.__user_payload.state_issuer,
            telephone=self.__user_payload.telephone,
            vehicles=self.__user_payload.vehicles,
        )

        user_creation_service.execute()

    def test_auth(self) -> None:
        user_auth_props: Mock = Mock()

        user_auth_props.email = self.__user_payload.email
        user_auth_props.password = self.__user_payload.password

        user_auth_service: IService[str] = UserAuthenticationService(
            email=user_auth_props.email, password=user_auth_props.password
        )

        token: str = user_auth_service.execute()

        self.assertTrue(token)

    def test_update(self) -> None:
        self.__user_payload.id_uuid = "ebd913c9-cd40-4822-af1f-822732cff2c4"

        update_service: IService[None] = UserUpdateService(
            user_uuid=self.__user_payload.id_uuid,
            name=self.__user_payload.name,
            email=self.__user_payload.email,
            password=self.__user_payload.password,
            document=self.__user_payload.document,
            birthday=self.__user_payload.birthday,
            address_city=self.__user_payload.address_city,
            address_district=self.__user_payload.address_district,
            address_number=self.__user_payload.address_number,
            address_state=self.__user_payload.address_state,
            address_street=self.__user_payload.address_street,
            document_rg=self.__user_payload.document_rg,
            state_issuer=self.__user_payload.state_issuer,
            telephone=self.__user_payload.telephone,
        )

        update_service.execute()

    def test_exclusion(self) -> None:
        self.__user_payload.id_uuid = "ebd913c9-cd40-4822-af1f-822732cff2c4"

        exclusion_service: IService[None] = UserExclusionService(
            user_uuid=self.__user_payload.id_uuid
        )

        exclusion_service.execute()
