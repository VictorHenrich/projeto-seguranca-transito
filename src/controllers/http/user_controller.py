from typing import Mapping, Any, Collection
from dataclasses import dataclass
from datetime import date

from server import App
from server.http import (
    Controller,
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
    nome: str
    email: str
    senha: str
    cpf: str
    rg: str
    estado_emissor: str
    telefone: str
    data_nascimento: str
    endereco_uf: str
    endereco_cidade: str
    endereco_bairro: str
    endereco_logradouro: str
    endereco_numero: str
    veiculos: Collection[Mapping[str, Any]]


@dataclass
class UserUpdateBody:
    nome: str
    email: str
    senha: str
    cpf: str
    rg: str
    estado_emissor: str
    telefone: str
    data_nascimento: str
    endereco_uf: str
    endereco_cidade: str
    endereco_bairro: str
    endereco_logradouro: str
    endereco_numero: str


body_request_middleware: BodyRequestValidationMiddleware = (
    BodyRequestValidationMiddleware()
)
user_auth_middleware: UserAuthenticationMiddleware = UserAuthenticationMiddleware()


@App.http.add_controller("/usuario/registro", "/usuario/registro/<uuid:user_hash>")
class UserController(Controller):
    @body_request_middleware.apply(BodyRequestValidationProps(UserCreateBody))
    def post(self, body_request: UserCreateBody) -> ResponseDefaultJSON:
        try:
            birthday: date = DateUtils.parse_string_to_datetime(
                body_request.data_nascimento
            ).date()

        except:
            return ResponseFailure(data="Data passada é inválida!")
        

        try:
            vehicles: Collection[Mapping[str, Any]] = [
                {
                    "plate": v["placa"],
                    "renavam": v["renavam"],
                    "vehicle_type": v["tipo_veiculo"],
                    "model": v.get("modelo"),
                    "color": v.get("color"),
                    "year": v.get("year"),
                    "brand": v.get("marca"),
                    "have_safe": v.get("possui_seguro")
                }
                for v in body_request.veiculos
            ]

        except KeyError:
            return ResponseFailure(data="Lista de veículos passados é inválido!")

        service: IService[User] = UserCreationService(
            name=body_request.nome,
            email=body_request.email,
            password=body_request.senha,
            document=body_request.cpf,
            document_rg=body_request.rg,
            state_issuer=body_request.estado_emissor,
            telephone=body_request.telefone,
            birthday=birthday,
            address_state=body_request.endereco_uf,
            address_city=body_request.endereco_cidade,
            address_district=body_request.endereco_bairro,
            address_street=body_request.endereco_logradouro,
            address_number=body_request.endereco_numero,
            vehicles=vehicles,
        )

        service.execute()

        return ResponseSuccess()

    @user_auth_middleware.apply()
    @body_request_middleware.apply(BodyRequestValidationProps(UserUpdateBody))
    def put(self, auth: User, body_request: UserUpdateBody) -> ResponseDefaultJSON:
        try:
            birthday: date = DateUtils.parse_string_to_datetime(
                body_request.data_nascimento
            ).date()

        except:
            return ResponseFailure(data="Data passada é inválida!")

        service: IService[None] = UserUpdateService(
            name=body_request.nome,
            email=body_request.email,
            password=body_request.senha,
            document=body_request.cpf,
            document_rg=body_request.rg,
            state_issuer=body_request.estado_emissor,
            telephone=body_request.telefone,
            birthday=birthday,
            address_state=body_request.endereco_uf,
            address_city=body_request.endereco_cidade,
            address_district=body_request.endereco_bairro,
            address_street=body_request.endereco_logradouro,
            address_number=body_request.endereco_numero,
            user_uuid=auth.id_uuid,
        )

        service.execute()

        return ResponseSuccess()

    @user_auth_middleware.apply()
    def delete(self, auth: User) -> ResponseDefaultJSON:
        service: IService[None] = UserExclusionService(user_uuid=auth.id_uuid)

        service.execute()

        return ResponseSuccess()

    @user_auth_middleware.apply()
    def get(self, auth: User) -> ResponseDefaultJSON:
        response: Mapping[str, Any] = {
            "nome": auth.nome,
            "email": auth.email,
            "cpf": auth.cpf,
            "uuid": auth.id_uuid,
            "data_nascimento": auth.data_nascimento,
        }

        return ResponseSuccess(data=response)
