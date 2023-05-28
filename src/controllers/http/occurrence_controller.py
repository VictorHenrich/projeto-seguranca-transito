from typing import Mapping, Any, Collection, Optional
from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

from flask import Response

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
    OccurrenceExclusionService,
    OccurrenceGettingService,
    OccurrenceListingService,
)
from utils import DateUtils


@dataclass
class OccurrenceCreatePayload:
    user_uuid: str
    vehicle_uuid: str
    description: str
    lat: str
    lon: str
    attachments: Collection[Mapping[str, Any]] = []
    created: Optional[str] = None


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
    OccurrenceCreatePayload
)


@App.http.add_controller(
    "/ocorrencia/registro",
    "/ocorrencia/registro/<uuid:occurrence_hash>",
)
class OccurrenceController(Controller):
    @user_auth_middleware.apply()
    @body_request_middleware.apply(occurrence_create_props)
    def post(
        self, auth: User, body_request: OccurrenceCreatePayload
    ) -> ResponseDefaultJSON:

        try:
            created: datetime = DateUtils.parse_string_to_datetime(
                body_request.created or ""
            )

        except:
            created: datetime = datetime.utcnow()

        occurrence_creation_service: IService[None] = OccurrenceCreationService(
            user_uuid=auth.id_uuid,
            vehicle_uuid=body_request.vehicle_uuid,
            attachments=body_request.attachments,
            description=body_request.description,
            lat=body_request.lat,
            lon=body_request.lon,
            created=created,
        )

        occurrence_creation_service.execute()

        return ResponseSuccess()

    @user_auth_middleware.apply()
    def delete(self, occurrence_hash: UUID, auth: User) -> Response:
        occurrence_exclusion_service: IService[None] = OccurrenceExclusionService(
            str(occurrence_hash)
        )

        occurrence_exclusion_service.execute()

        return ResponseSuccess()


@App.http.add_controller("/ocorrencia/busca")
class OccurrenceListController(Controller):
    @user_auth_middleware.apply()
    def get(self, auth: User) -> Response:
        occurrence_listing_service: IService[
            Collection[Mapping[str, Any]]
        ] = OccurrenceListingService(auth)

        occurrences: Collection[
            Mapping[str, Any]
        ] = occurrence_listing_service.execute()

        return ResponseSuccess(data=occurrences)


@App.http.add_controller("/ocorrencia/busca/<uuid:occurrence_hash>")
class OccurrenceGetController(Controller):
    @user_auth_middleware.apply()
    def get(self, occurrence_hash: UUID, auth: User) -> Response:
        occurrence_listing_service: IService[
            Mapping[str, Any]
        ] = OccurrenceGettingService(str(occurrence_hash))

        occurrence: Mapping[str, Any] = occurrence_listing_service.execute()

        return ResponseSuccess(data=occurrence)
