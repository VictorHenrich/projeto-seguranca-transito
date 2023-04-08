from dataclasses import dataclass

from server import App
from server.http import Controller, ResponseDefaultJSON, ResponseSuccess
from middlewares.http import BodyRequestValidationMiddleware, BodyRequestValidationProps
from patterns.service import IService
from services.departament import (
    DepartamentCreationService,
    DepartamentCreationServiceProps,
)


@dataclass
class DepartamentCreationBodyRequest:
    nome: str
    unidade: str
    acesso: str
    cep: str
    uf: str
    cidade: str
    bairro: str
    logradouro: str
    complemento: str


body_request_middleware: BodyRequestValidationMiddleware = (
    BodyRequestValidationMiddleware()
)
body_request_props: BodyRequestValidationProps = BodyRequestValidationProps(
    DepartamentCreationBodyRequest
)


@App.http.add_controller("/departamento/crud")
class CrudDepartamentoController(Controller):
    @body_request_middleware.apply(body_request_props)
    def post(self, body_request: DepartamentCreationBodyRequest) -> ResponseDefaultJSON:
        departament_creating_service: IService[
            DepartamentCreationServiceProps, None
        ] = DepartamentCreationService()

        departament_creation_service_props: DepartamentCreationServiceProps = (
            DepartamentCreationServiceProps(
                name=body_request.nome,
                unit=body_request.unidade,
                access=body_request.acesso,
                zipcode=body_request.cep,
                state=body_request.uf,
                city=body_request.cidade,
                district=body_request.bairro,
                street=body_request.logradouro,
                complement=body_request.complemento,
            )
        )

        departament_creating_service.execute(departament_creation_service_props)

        return ResponseSuccess()
