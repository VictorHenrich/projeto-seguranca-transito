from typing import Mapping, Any
from services.http import Controller, ResponseSuccess, ResponseDefaultJSON, ResponseFailure
from middlewares import DepartamentUserAuthenticationMiddleware, BodyRequestValidationMiddleware
from repositories import OccurrenceRepository, UserRepository
from patterns.ocorrencia import OccurrenceView, OccurrenceRegistration
from models import (
    Ocorrencia,
    UsuarioDepartamento,
    Departamento
)
from exceptions import (
    OccurrenceNotFoundError,
    UserNotFoundError
)



class CrudOcorrenciaController(Controller):
    @DepartamentUserAuthenticationMiddleware
    def get(
        self,
        auth_user: UsuarioDepartamento,
        auth_departament: Departamento
    ) -> ResponseDefaultJSON:
        ocorrencias: list[Ocorrencia] = OccurrenceRepository.fetch(
            auth_departament
        )

        resposta_json: list[Mapping[str, Any]] = [
            OccurrenceView(
                ocorrencia.descricao,
                ocorrencia.obs,
                ocorrencia.status,
                ocorrencia.id_uuid
            ).__dict__

            for ocorrencia in ocorrencias
        ]

        return ResponseSuccess(data=resposta_json)

    @DepartamentUserAuthenticationMiddleware.apply()
    @BodyRequestValidationMiddleware.apply(OccurrenceRegistration)
    def post(
        self,
        auth_user: UsuarioDepartamento,
        auth_departament: Departamento,
        body_request: OccurrenceRegistration
    ) -> ResponseDefaultJSON:
        try:
            OccurrenceRepository.create(
                auth_departament,
                body_request
            )

        except UserNotFoundError as error:
            return ResponseFailure(data=str(error))

        except OccurrenceNotFoundError as error:
            return ResponseFailure(data=str(error))

        else:
            return ResponseSuccess()

    @DepartamentUserAuthenticationMiddleware.apply()
    @BodyRequestValidationMiddleware.apply(OccurrenceRegistration)
    def put(
        self,
        hash_occurrence: str,
        auth_user: UsuarioDepartamento,
        auth_departament: Departamento,
        body_request: OccurrenceRegistration
    ) -> ResponseDefaultJSON:
        try:
            OccurrenceRepository.update(
                hash_occurrence,
                auth_departament,
                body_request
            )

        except OccurrenceNotFoundError as error:
            return ResponseFailure(data=str(error))

        else:
            return ResponseSuccess()

    @DepartamentUserAuthenticationMiddleware.apply()
    def delete(
        self,
        hash_occurrence: str,
        auth_user: UsuarioDepartamento,
        auth_departament: Departamento,
    ) -> ResponseDefaultJSON:
        try:
            OccurrenceRepository.delete(
                hash_occurrence,
                auth_departament
            )

        except OccurrenceNotFoundError as error:
            return ResponseFailure(data=str(error))

        else:
            return ResponseSuccess()

