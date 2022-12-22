from typing import Mapping, Any, Optional
from dataclasses import dataclass

from server.http import (
    Controller,
    ResponseDefaultJSON,
    ResponseSuccess,
)
from middlewares import BodyRequestValidationMiddleware, UserAuthenticationMiddleware
from models import Usuario
from patterns.service import IService
from services.user import (
    UserCreationService,
    UserGettingService,
    UserExclusionService,
    UserUpdateService
)



@dataclass
class UserRegistrationRequestBody:
    nome: str
    email: str
    cpf: str
    senha: str
    data_aniversario: Optional[None] = None


class CrudUsuariosController(Controller):
    @BodyRequestValidationMiddleware.apply(UserRegistrationRequestBody)
    def post(
        self, 
        body_request: UserRegistrationRequestBody
    ) -> ResponseDefaultJSON:
        service: IService[None] = UserCreationService()

        service.execute(
            name=body_request.nome,
            document=body_request.cpf,
            birthday=body_request.data_aniversario,
            email=body_request.email,
            password=body_request.senha
        )

        return ResponseSuccess()

    @UserAuthenticationMiddleware.apply()
    @BodyRequestValidationMiddleware.apply(UserRegistrationRequestBody)
    def put(
        self, 
        auth: Usuario, 
        body_request: UserRegistrationRequestBody
    ) -> ResponseDefaultJSON:
        service: IService[None] = UserUpdateService()

        service.execute(
            name=body_request.nome,
            document=body_request.cpf,
            birthday=body_request.data_aniversario,
            email=body_request.email,
            password=body_request.senha,
            uuid_user=auth.id_uuid
        )

        return ResponseSuccess()

    @UserAuthenticationMiddleware.apply()
    def delete(
        self, 
        auth: Usuario
    ) -> ResponseDefaultJSON:
        service: IService[None] = UserExclusionService()

        service.execute(uuid_user=auth.id_uuid)

        return ResponseSuccess()

    @UserAuthenticationMiddleware.apply()
    def get(
        self,  
        auth: Usuario
    ) -> ResponseDefaultJSON:
        service: IService[Usuario] = UserGettingService()
        
        user: Usuario = service.execute(uuid_user=auth.id_uuid)

        response: Mapping[str, Any] = {
            "nome": user.nome,
            "email": user.email,
            "cpf": user.cpf,
            "uuid": user.id_uuid,
            "data_nascimento": user.data_nascimento
        }

        return ResponseSuccess(data=response)
