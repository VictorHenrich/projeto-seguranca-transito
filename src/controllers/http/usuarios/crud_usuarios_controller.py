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
from models import Usuario
from patterns.service import IService
from services.user import (
    UserCreationService,
    UserGettingService,
    UserExclusionService,
    UserUpdateService,
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
        service: IService[None] = UserCreationService()

        service.execute(
            name=body_request.nome,
            document=body_request.cpf,
            birthday=body_request.data_nascimento,
            email=body_request.email,
            password=body_request.senha,
        )

        return ResponseSuccess()

    @UserAuthenticationMiddleware.apply()
    @BodyRequestValidationMiddleware.apply(UserRegistrationRequestBody)
    def put(
        self, auth: Usuario, body_request: UserRegistrationRequestBody
    ) -> ResponseDefaultJSON:
        service: IService[None] = UserUpdateService()

        service.execute(
            name=body_request.nome,
            document=body_request.cpf,
            birthday=body_request.data_nascimento,
            email=body_request.email,
            password=body_request.senha,
            uuid_user=auth.id_uuid,
        )

        return ResponseSuccess()

    @UserAuthenticationMiddleware.apply()
    def delete(self, auth: Usuario) -> ResponseDefaultJSON:
        service: IService[None] = UserExclusionService()

        service.execute(uuid_user=auth.id_uuid)

        return ResponseSuccess()

    @UserAuthenticationMiddleware.apply()
    def get(self, auth: Usuario) -> ResponseDefaultJSON:
        service: IService[Usuario] = UserGettingService()

        user: Usuario = service.execute(uuid_user=auth.id_uuid)

        response: Dict[str, Any] = {
            "nome": user.nome,
            "email": user.email,
            "cpf": user.cpf,
            "uuid": user.id_uuid,
            "data_nascimento": user.data_nascimento,
        }

        return ResponseSuccess(data=response)
