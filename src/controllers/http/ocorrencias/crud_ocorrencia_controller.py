from typing import List, Dict, Any
from dataclasses import dataclass
from uuid import UUID

from start import app
from patterns.service import IService
from server.http import Controller, ResponseDefaultJSON, ResponseSuccess
from middlewares.http import (
    BodyRequestValidationMiddleware,
    UserAuthenticationMiddleware,
)
from models import User, Occurrence
from services.occurrence import (
    OccurrenceCreationService,
    OccurrenceExclusionService,
    OccurrenceUpdateService,
    OccurrenceListingService,
)


@dataclass
class OccurrenceCreationBodyRequest:
    descricao: str
    obs: str
    uuid_departamento: str


@dataclass
class OccurrenceUpdateBodyRequest:
    descricao: str
    obs: str


@app.http.add_controller(
    "/ocorrencia/crud",
    "/ocorrencia/crud/<uuid:occurrence_hash>",
)
class CrudOcorrenciasController(Controller):
    @UserAuthenticationMiddleware.apply()
    @BodyRequestValidationMiddleware.apply(OccurrenceCreationBodyRequest)
    def post(
        self, auth: User, body_request: OccurrenceCreationBodyRequest
    ) -> ResponseDefaultJSON:
        occurrence_creation_service: IService[None] = OccurrenceCreationService()

        occurrence_creation_service.execute(
            user=auth,
            uuid_departament=body_request.uuid_departamento,
            description=body_request.descricao,
            obs=body_request.obs,
        )

        return ResponseSuccess()

    @UserAuthenticationMiddleware.apply()
    @BodyRequestValidationMiddleware.apply(OccurrenceUpdateBodyRequest)
    def put(
        self,
        occurrence_hash: UUID,
        auth: User,
        body_request: OccurrenceUpdateBodyRequest,
    ) -> ResponseDefaultJSON:
        occurrence_update_service: IService[None] = OccurrenceUpdateService()

        occurrence_update_service.execute(
            uuid_occurrence=str(occurrence_hash),
            description=body_request.descricao,
            obs=body_request.obs,
        )

        return ResponseSuccess()

    @UserAuthenticationMiddleware.apply()
    def delete(self, occurrence_hash: UUID, auth: User) -> ResponseDefaultJSON:
        occurrence_exclusion_service: IService[None] = OccurrenceExclusionService()

        occurrence_exclusion_service.execute(uuid_occurrence=str(occurrence_hash))

        return ResponseSuccess()

    @UserAuthenticationMiddleware.apply()
    def get(self, auth: User) -> ResponseDefaultJSON:
        occurrence_listing_service: IService[
            List[Occurrence]
        ] = OccurrenceListingService()

        occurrences: List[Occurrence] = occurrence_listing_service.execute(user=auth)

        response: List[Dict[str, Any]] = [
            {
                "description": occurrence.descricao,
                "obs": occurrence.obs,
                "uuid": occurrence.id_uuid,
            }
            for occurrence in occurrences
        ]

        return ResponseSuccess(data=response)
