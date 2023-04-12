from typing import List, Dict, Any
from dataclasses import dataclass
from uuid import UUID

from server import App
from patterns.service import IService
from server.http import Controller, ResponseDefaultJSON, ResponseSuccess
from middlewares.http import (
    BodyRequestValidationMiddleware,
    BodyRequestValidationProps,
    UserAuthenticationMiddleware,
)
from models import User, Occurrence
from services.occurrence import (
    OccurrenceCreationService,
    OccurrenceCreationServiceProps,
    OccurrenceExclusionService,
    OccurrenceExclusionServiceProps,
    OccurrenceUpdateService,
    OccurrenceUpdateServiceProps,
    OccurrenceListingService,
    OccurrenceListingServiceProps,
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


body_request_middleware: BodyRequestValidationMiddleware = (
    BodyRequestValidationMiddleware()
)
user_auth_middleware: UserAuthenticationMiddleware = UserAuthenticationMiddleware()

occurrence_update_props: BodyRequestValidationProps = BodyRequestValidationProps(
    OccurrenceUpdateBodyRequest
)
occurrence_create_props: BodyRequestValidationProps = BodyRequestValidationProps(
    OccurrenceCreationBodyRequest
)


@App.http.add_controller(
    "/ocorrencia/crud",
    "/ocorrencia/crud/<uuid:occurrence_hash>",
)
class OccurrenceCrudController(Controller):
    @user_auth_middleware.apply(None)
    @body_request_middleware.apply(occurrence_create_props)
    def post(
        self, auth: User, body_request: OccurrenceCreationBodyRequest
    ) -> ResponseDefaultJSON:
        occurrence_creation_service: IService[
            OccurrenceCreationServiceProps, None
        ] = OccurrenceCreationService()

        occurrence_creation_service_props: OccurrenceCreationServiceProps = (
            OccurrenceCreationServiceProps(
                user=auth,
                uuid_departament=body_request.uuid_departamento,
                description=body_request.descricao,
                obs=body_request.obs,
            )
        )

        occurrence_creation_service.execute(occurrence_creation_service_props)

        return ResponseSuccess()

    @user_auth_middleware.apply(None)
    @body_request_middleware.apply(occurrence_update_props)
    def put(
        self,
        occurrence_hash: UUID,
        auth: User,
        body_request: OccurrenceUpdateBodyRequest,
    ) -> ResponseDefaultJSON:
        occurrence_update_service: IService[
            OccurrenceUpdateServiceProps, None
        ] = OccurrenceUpdateService()

        occurrence_update_service_props: OccurrenceUpdateServiceProps = (
            OccurrenceUpdateServiceProps(
                uuid_occurrence=str(occurrence_hash),
                description=body_request.descricao,
                obs=body_request.obs,
            )
        )

        occurrence_update_service.execute(occurrence_update_service_props)

        return ResponseSuccess()

    @user_auth_middleware.apply(None)
    def delete(self, occurrence_hash: UUID, auth: User) -> ResponseDefaultJSON:
        occurrence_exclusion_service: IService[
            OccurrenceExclusionServiceProps, None
        ] = OccurrenceExclusionService()

        occurrence_exclusion_service_props: OccurrenceExclusionServiceProps = (
            OccurrenceExclusionServiceProps(uuid_occurrence=str(occurrence_hash))
        )

        occurrence_exclusion_service.execute(occurrence_exclusion_service_props)

        return ResponseSuccess()

    @user_auth_middleware.apply(None)
    def get(self, auth: User) -> ResponseDefaultJSON:
        occurrence_listing_service: IService[
            OccurrenceListingServiceProps, List[Occurrence]
        ] = OccurrenceListingService()

        occurrence_listing_service_props: OccurrenceListingServiceProps = (
            OccurrenceListingServiceProps(user=auth)
        )

        occurrences: List[Occurrence] = occurrence_listing_service.execute(
            occurrence_listing_service_props
        )

        response: List[Dict[str, Any]] = [
            {
                "description": occurrence.descricao,
                "obs": occurrence.obs,
                "uuid": occurrence.id_uuid,
            }
            for occurrence in occurrences
        ]

        return ResponseSuccess(data=response)
