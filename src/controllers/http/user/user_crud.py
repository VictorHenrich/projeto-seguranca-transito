from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

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
    UserCreationServiceProps,
    UserFindingService,
    UserFindingServiceProps,
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
    data_nascimento: Optional[str] = None
    status: bool = True


body_request_middleware: BodyRequestValidationMiddleware = (
    BodyRequestValidationMiddleware()
)
user_auth_middleware: UserAuthenticationMiddleware = UserAuthenticationMiddleware()

body_request_params: BodyRequestValidationProps = BodyRequestValidationProps(
    UserRegistrationRequestBody
)


@App.http.add_controller("/usuario/crud", "/usuario/crud/<uuid:user_hash>")
class UserCrudController(Controller):
    @body_request_middleware.apply(body_request_params)
    def post(self, body_request: UserRegistrationRequestBody) -> ResponseDefaultJSON:
        service: IService[UserCreationServiceProps, None] = UserCreationService()

        service_props: UserCreationServiceProps = UserCreationServiceProps(
            name=body_request.nome,
            document=body_request.cpf,
            birthday=None,
            email=body_request.email,
            password=body_request.senha,
        )

        service.execute(service_props)

        return ResponseSuccess()

    @user_auth_middleware.apply(None)
    @body_request_middleware.apply(body_request_params)
    def put(
        self, auth: User, body_request: UserRegistrationRequestBody
    ) -> ResponseDefaultJSON:
        service: IService[UserUpdateServiceProps, None] = UserUpdateService()

        service_props: UserUpdateServiceProps = UserUpdateServiceProps(
            name=body_request.nome,
            document=body_request.cpf,
            birthday=datetime.now().date(),
            email=body_request.email,
            password=body_request.senha,
            user_uuid=auth.id_uuid,
            status=body_request.status,
        )

        service.execute(service_props)

        return ResponseSuccess()

    @user_auth_middleware.apply(None)
    def delete(self, auth: User) -> ResponseDefaultJSON:
        service: IService[UserExclusionServiceProps, None] = UserExclusionService()

        service_props: UserExclusionServiceProps = UserExclusionServiceProps(
            user_uuid=auth.id_uuid
        )

        service.execute(service_props)

        return ResponseSuccess()

    @user_auth_middleware.apply(None)
    def get(self, auth: User) -> ResponseDefaultJSON:
        service: IService[UserFindingServiceProps, User] = UserFindingService()

        service_props: UserFindingServiceProps = UserFindingServiceProps(
            user_uuid=auth.id_uuid
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
