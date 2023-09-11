from typing import Mapping, Any, Optional, Collection, Literal, Union
from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from flask import Response

from server import HttpServer
from patterns.service import IService
from server.http import HttpController, ResponseDefaultJSON, ResponseSuccess
from models import User
from src.server.http.responses_default import ResponseFailure
from utils import DateUtils
from utils.entities import LocationPayload, AddressPayload, AttachmentPayload
from middlewares.http import (
    BodyRequestValidationMiddleware,
    BodyRequestValidationProps,
    UserAuthenticationMiddleware,
)
from services.occurrence import (
    OccurrenceCreationService,
    OccurrenceExclusionService,
    OccurrenceGettingService,
    OccurrenceAggregationService,
)


@dataclass
class OccurrenceCreatePayload:
    vehicle_uuid: str
    description: str
    location: Optional[Mapping[Literal["lat", "lon"], Union[str, float]]]
    address: Optional[Mapping[str, Any]]
    attachments: Collection[Mapping[Literal["content", "type"], Any]]
    created: Optional[str] = None


@dataclass
class OccurrenceUpdateBodyRequest:
    description: str
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


@HttpServer.add_controller(
    "/user/occurrence/register",
    "/user/occurrence/register/<uuid:occurrence_hash>",
)
class OccurrenceRegisterController(HttpController):
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

        attachments: Collection[AttachmentPayload] = [
            AttachmentPayload(content=attachment["content"], type=attachment["type"])
            for attachment in body_request.attachments
        ]

        if body_request.address:
            address: Union[AddressPayload, LocationPayload] = AddressPayload(
                zipcode=body_request.address["zipcode"],
                state=body_request.address["state"],
                city=body_request.address["city"],
                district=body_request.address["district"],
                street=body_request.address["street"],
                number=body_request.address["number"],
            )

        elif body_request.location:
            address: Union[AddressPayload, LocationPayload] = LocationPayload(
                body_request.location["lat"], body_request.location["lon"]
            )

        else:
            return ResponseFailure(
                data="Parametro de endereço não informado para o cadastro!"
            )

        occurrence_creation_service: IService[None] = OccurrenceCreationService(
            user_uuid=auth.id_uuid,
            vehicle_uuid=body_request.vehicle_uuid,
            attachments=attachments,
            description=body_request.description,
            address=address,
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


@HttpServer.add_controller("/user/occurrence/query")
class OccurrenceQueryManyController(HttpController):
    @user_auth_middleware.apply()
    def get(self, auth: User) -> Response:
        occurrence_listing_service: IService[
            Collection[Mapping[str, Any]]
        ] = OccurrenceAggregationService(auth)

        occurrences: Collection[
            Mapping[str, Any]
        ] = occurrence_listing_service.execute()

        return ResponseSuccess(data=occurrences)


@HttpServer.add_controller("/user/occurrence/query/<uuid:occurrence_hash>")
class OccurrenceQueryOneController(HttpController):
    @user_auth_middleware.apply()
    def get(self, occurrence_hash: UUID, auth: User) -> Response:
        occurrence_listing_service: IService[
            Mapping[str, Any]
        ] = OccurrenceGettingService(str(occurrence_hash))

        occurrence: Mapping[str, Any] = occurrence_listing_service.execute()

        return ResponseSuccess(data=occurrence)
