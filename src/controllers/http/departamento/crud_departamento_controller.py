from dataclasses import dataclass

from start import app
from server.http import Controller, ResponseDefaultJSON, ResponseSuccess
from middlewares.http import BodyRequestValidationMiddleware
from patterns.service import IService
from services.departament import DepartamentCreationService


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


@app.http.add_controller("/departamento/crud")
class CrudDepartamentoController(Controller):
    @BodyRequestValidationMiddleware.apply(DepartamentCreationBodyRequest)
    def post(self, body_request: DepartamentCreationBodyRequest) -> ResponseDefaultJSON:
        departament_creating_service: IService[None] = DepartamentCreationService()

        departament_creating_service.execute(
            name=body_request.nome,
            unit=body_request.unidade,
            access=body_request.acesso,
            cep=body_request.cep,
            uf=body_request.uf,
            city=body_request.cidade,
            district=body_request.bairro,
            street=body_request.logradouro,
            complement=body_request.complemento,
        )

        return ResponseSuccess()
