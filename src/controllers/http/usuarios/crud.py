from typing import Mapping, Any
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
class UserRequestBody:
    pass



class CrudUsuariosController(Controller):
    @BodyRequestValidationMiddleware.apply(UserRequestBody)
    def post(
        self, 
        body_request: UserRequestBody
    ) -> ResponseDefaultJSON:
        service: IService[None] = UserCreationService()

        service.execute(**body_request.__dict__)

        return ResponseSuccess()

    @UserAuthenticationMiddleware.apply()
    @BodyRequestValidationMiddleware.apply(UserRequestBody)
    def put(
        self, 
        auth: Usuario, 
        body_request: UserRequestBody
    ) -> ResponseDefaultJSON:
        service: IService[None] = UserUpdateService()

        service.execute(
            **body_request.__dict__, 
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
