from typing import Dict, Any, Optional
from dataclasses import dataclass

from start import app
from server.http import (
    Controller,
    ResponseDefaultJSON,
    ResponseSuccess,
)
from middlewares.http import (
    BodyRequestValidationMiddleware,
    UserAuthenticationMiddleware,
)
from models import User
from patterns.service import IService
from services.user import (
    UserCreationService,
    UserCreationServiceProps,
    UserGettingService,
    UserGettingServiceProps,
    UserExclusionService,
    UserExclusionServiceProps,
    UserUpdateService,
    UserUpdateServiceProps,
)


@dataclass
class UserRegistrationRequestBody:
    nome: str
    email: str
    cpf: str
    senha: str
    data_nascimento: Optional[None] = None


@app.http.add_controller("/usuario/crud", "/usuario/crud/<uuid:user_hash>")
class CrudUsuariosController(Controller):
    @BodyRequestValidationMiddleware.apply(UserRegistrationRequestBody)
    def post(self, body_request: UserRegistrationRequestBody) -> ResponseDefaultJSON:
        service: IService[UserCreationServiceProps, None] = UserCreationService()

        service_props: UserCreationServiceProps = UserCreationServiceProps(
            name=body_request.nome,
            document=body_request.cpf,
            birthday=body_request.data_nascimento,
            email=body_request.email,
            password=body_request.senha,
        )

        service.execute(service_props)

        return ResponseSuccess()

    @UserAuthenticationMiddleware.apply()
    @BodyRequestValidationMiddleware.apply(UserRegistrationRequestBody)
    def put(
        self, auth: User, body_request: UserRegistrationRequestBody
    ) -> ResponseDefaultJSON:
        service: IService[UserUpdateServiceProps, None] = UserUpdateService()

        service_props: UserUpdateServiceProps = UserUpdateServiceProps(
            name=body_request.nome,
            document=body_request.cpf,
            birthday=body_request.data_nascimento,
            email=body_request.email,
            password=body_request.senha,
            uuid_user=auth.id_uuid,
        )

        service.execute(service_props)

        return ResponseSuccess()

    @UserAuthenticationMiddleware.apply()
    def delete(self, auth: User) -> ResponseDefaultJSON:
        service: IService[UserExclusionServiceProps, None] = UserExclusionService()

        service_props: UserExclusionServiceProps = UserExclusionServiceProps(
            uuid_ser=auth.id_uuid
        )

        service.execute(service_props)

        return ResponseSuccess()

    @UserAuthenticationMiddleware.apply()
    def get(self, auth: User) -> ResponseDefaultJSON:
        service: IService[UserGettingServiceProps, User] = UserGettingService()

        service_props: UserGettingServiceProps = UserGettingServiceProps(
            uuid_user=auth.id_uuid
        )

        user: User = service.execute(service_props)

        response: Dict[str, Any] = {
            "nome": user.nome,
            "email": user.email,
            "cpf": user.cpf,
            "uuid": user.id_uuid,
            "data_nascimento": user.data_nascimento,
        }

        return ResponseSuccess(data=response)
