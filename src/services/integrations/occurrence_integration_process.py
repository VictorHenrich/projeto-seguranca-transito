from typing import Tuple, TypeAlias, Literal, Collection
from dataclasses import dataclass
from sqlalchemy.orm import Session
import logging

from server import App
from patterns.repository import (
    IAggregateRepository,
    IUpdateRepository,
    IFindManyRepository,
)
from repositories.occurrence import (
    OccurrenceAggregateRepository,
    OccurrenceAggregateRepositoryParams,
    OccurrenceUpdateStatusRepository,
    OccurrenceUpdateStatusRepositoryParams,
)
from repositories.attachment import (
    AttachmentFindManyRepository,
    AttachmentFindManyRepositoryParams,
)
from models import Occurrence, User, Vehicle, Attachment
from patterns.service.iservice import IService
from .occurrence_integration_creation import OccurrenceIntegrationCreationService


OccurrenceLoad: TypeAlias = Tuple[Occurrence, User, Vehicle]

OccurrenceStatus: TypeAlias = Literal["ANDAMENTO", "PROCESSO", "FALHA", "SUCESSO"]


@dataclass
class OccurrenceAggregateProps:
    occurrence_uuid: str


@dataclass
class OccurrenceUpdateStatusProps:
    occurrence: Occurrence
    status: OccurrenceStatus


@dataclass
class AttachmentFindProps:
    occurrence: Occurrence


class OccurrenceIntegrationProcessService:
    def __init__(self, ocurrence_uuid: str) -> None:
        self.__occurrence_uuid: str = ocurrence_uuid

    def __find_attachments(
        self, session: Session, occurrence: Occurrence
    ) -> Collection[Attachment]:
        attach_find_many_repo: IFindManyRepository[
            AttachmentFindManyRepositoryParams, Collection[Attachment]
        ] = AttachmentFindManyRepository(session)

        return attach_find_many_repo.find_many(AttachmentFindProps(occurrence))

    def __aggregate_occurrence(self, session: Session) -> OccurrenceLoad:
        occurrence_load_repository: IAggregateRepository[
            OccurrenceAggregateRepositoryParams, OccurrenceLoad
        ] = OccurrenceAggregateRepository(session)

        occurrence_aggregate_props: OccurrenceAggregateProps = OccurrenceAggregateProps(
            self.__occurrence_uuid
        )

        return occurrence_load_repository.aggregate(occurrence_aggregate_props)

    def __update_occurrence_status(
        self, session: Session, occurrence: Occurrence, status: OccurrenceStatus
    ) -> None:
        occurrence_update_service: IUpdateRepository[
            OccurrenceUpdateStatusRepositoryParams, None
        ] = OccurrenceUpdateStatusRepository(session)

        occurrence_update_props: OccurrenceUpdateStatusProps = (
            OccurrenceUpdateStatusProps(occurrence, status)
        )

        occurrence_update_service.update(occurrence_update_props)

    def __integration_occurrence(
        self,
        user: User,
        vehicle: Vehicle,
        occurrence: Occurrence,
        attachments: Collection[Attachment],
    ) -> None:
        occurrence_integration_service: IService[
            None
        ] = OccurrenceIntegrationCreationService(occurrence, user, vehicle, attachments)

        occurrence_integration_service.execute()

    def execute(self) -> None:
        with App.databases.create_session() as session:
            occurrence, user, vehicle = self.__aggregate_occurrence(session)

            attachments: Collection[Attachment] = self.__find_attachments(
                session, occurrence
            )

            logging.info(f"Dados de ocorrência localizados em: {occurrence.id_uuid}")

            self.__update_occurrence_status(session, occurrence, "PROCESSO")

            try:
                logging.info("Inicializando processamento de integração de ocorrência!")

                self.__integration_occurrence(user, vehicle, occurrence, attachments)

            except Exception as error:
                logging.error(
                    f"Falha ao realizar o processamento de integração de ocorrência: \n{error}"
                )

                self.__update_occurrence_status(session, occurrence, "FALHA")

            else:
                logging.info(
                    "Processamento de integração de ocorrência feita com sucesso!"
                )

                self.__update_occurrence_status(session, occurrence, "SUCESSO")

            session.commit()
