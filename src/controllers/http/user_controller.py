from typing import Mapping, Any, Collection
from dataclasses import dataclass
from datetime import date

from server import HttpServer
from server.http import (
    HttpController,
    ResponseDefaultJSON,
    ResponseSuccess,
)
from middlewares.http import (
    BodyRequestValidationMiddleware,
    BodyRequestValidationProps,
    UserAuthenticationMiddleware,
)
from models import User
from patterns.service import IService
from services.user import (
    UserCreationService,
    UserExclusionService,
    UserUpdateService,
)
from server.http.responses_default import ResponseFailure
from utils import DateUtils


@dataclass
class UserCreateBody:
    name: str
    email: str
    password: str
    document_cpf: str
    document_rg: str
    issuer_state: str
    telephone: str
    birthday: str
    address_state: str
    address_city: str
    address_district: str
    address_street: str
    address_number: str
    vehicles: Collection[Mapping[str, Any]]


@dataclass
class UserUpdateBody:
    name: str
    email: str
    password: str
    document_cpf: str
    document_rg: str
    issuer_state: str
    telephone: str
    birthday: str
    address_state: str
    address_city: str
    address_district: str
    address_street: str
    address_number: str


body_request_middleware: BodyRequestValidationMiddleware = (
    BodyRequestValidationMiddleware()
)
user_auth_middleware: UserAuthenticationMiddleware = UserAuthenticationMiddleware()


@HttpServer.add_controller("/user/register")
class UserRegisterController(HttpController):
    @body_request_middleware.apply(BodyRequestValidationProps(UserCreateBody))
    def post(self, body_request: UserCreateBody) -> ResponseDefaultJSON:
        try:
            birthday: date = DateUtils.parse_string_to_datetime(
                body_request.birthday
            ).date()

        except:
            return ResponseFailure(data="Data passada é inválida!")

        try:
            vehicles: Collection[Mapping[str, Any]] = [
                {
                    "plate": v["plate"],
                    "renavam": v["renavam"],
                    "vehicle_type": v["vehicle_type"],
                    "model": v.get("model"),
                    "color": v.get("color"),
                    "year": v.get("year"),
                    "brand": v.get("brand"),
                    "have_safe": v.get("have_safe"),
                }
                for v in body_request.vehicles
            ]

        except KeyError:
            return ResponseFailure(data="Lista de veículos passados é inválido!")

        service: IService[User] = UserCreationService(
            name=body_request.name,
            email=body_request.email,
            password=body_request.password,
            document=body_request.document_cpf,
            document_rg=body_request.document_rg,
            state_issuer=body_request.issuer_state,
            telephone=body_request.telephone,
            birthday=birthday,
            address_state=body_request.address_state,
            address_city=body_request.address_city,
            address_district=body_request.address_district,
            address_street=body_request.address_street,
            address_number=body_request.address_number,
            vehicles=vehicles,
        )

        service.execute()

        return ResponseSuccess()

    @user_auth_middleware.apply()
    @body_request_middleware.apply(BodyRequestValidationProps(UserUpdateBody))
    def put(self, auth: User, body_request: UserUpdateBody) -> ResponseDefaultJSON:
        try:
            birthday: date = DateUtils.parse_string_to_datetime(
                body_request.birthday
            ).date()

        except:
            return ResponseFailure(data="Data passada é inválida!")

        service: IService[None] = UserUpdateService(
            name=body_request.name,
            email=body_request.email,
            password=body_request.password,
            document=body_request.document_cpf,
            document_rg=body_request.document_rg,
            state_issuer=body_request.issuer_state,
            telephone=body_request.telephone,
            birthday=birthday,
            address_state=body_request.address_state,
            address_city=body_request.address_city,
            address_district=body_request.address_district,
            address_street=body_request.address_street,
            address_number=body_request.address_number,
            user_uuid=auth.id_uuid,
        )

        service.execute()

        return ResponseSuccess()

    @user_auth_middleware.apply()
    def delete(self, auth: User) -> ResponseDefaultJSON:
        service: IService[None] = UserExclusionService(user_uuid=auth.id_uuid)

        service.execute()

        return ResponseSuccess()


@HttpServer.add_controller("/user/query")
class UserQueryController(HttpController):
    @user_auth_middleware.apply()
    def get(self, auth: User) -> ResponseDefaultJSON:
        response: Mapping[str, Any] = {
            "uuid": auth.id_uuid,
            "name": auth.nome,
            "email": auth.email,
            "document_cpf": auth.cpf,
            "document_rg": auth.rg,
            "issuer_state": auth.estado_emissor,
            "address_state": auth.endereco_uf,
            "address_city": auth.endereco_cidade,
            "address_district": auth.endereco_bairro,
            "address_street": auth.endereco_logradouro,
            "address_number": auth.endereco_numero,
            "birthday": auth.data_nascimento,
        }

        return ResponseSuccess(data=response)
