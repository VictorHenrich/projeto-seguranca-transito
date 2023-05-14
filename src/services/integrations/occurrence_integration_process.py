from typing import Tuple, TypeAlias, Literal
from dataclasses import dataclass
from sqlalchemy.orm import Session

from server import App
from patterns.repository import IAggregateRepository, IUpdateRepository
from repositories.occurrence import (
    OccurrenceAggregateRepository,
    OccurrenceAggregateRepositoryParams,
    OccurrenceUpdateStatusRepository,
    OccurrenceUpdateStatusRepositoryParams,
)
from models import Occurrence, User, Vehicle


OccurrenceLoad: TypeAlias = Tuple[Occurrence, User, Vehicle]


@dataclass
class OccurrenceAggregateProps:
    occurrence_uuid: str


@dataclass
class OccurrenceUpdateStatusProps:
    occurrence_uuid: str
    status: Literal["ANDAMENTO", "PROCESSO", "FALHA", "SUCESSO"]


class OccurrenceIntegrationProcessService:
    def __init__(self, ocurrence_uuid: str) -> None:
        self.__occurrence_uuid: str = ocurrence_uuid

    def __aggregate_occurrence(self, session: Session) -> OccurrenceLoad:
        occurrence_load_repository: IAggregateRepository[
            OccurrenceAggregateRepositoryParams, OccurrenceLoad
        ] = OccurrenceAggregateRepository(session)

        occurrence_aggregate_props: OccurrenceAggregateProps = OccurrenceAggregateProps(
            self.__occurrence_uuid
        )

        return occurrence_load_repository.aggregate(occurrence_aggregate_props)

    def __update_occurrence_status(
        self, session: Session, occurrence: Occurrence
    ) -> None:
        occurrence_update_service: IUpdateRepository[
            OccurrenceUpdateStatusRepositoryParams, None
        ] = OccurrenceUpdateStatusRepository(session)

        occurrence_update_props: OccurrenceUpdateStatusProps = (
            OccurrenceUpdateStatusProps(occurrence.id_uuid, "PROCESSO")
        )

        occurrence_update_service.update(occurrence_update_props)

    def execute(self) -> None:
        with App.databases.create_session() as session:
            occurrence, user, vehicle = self.__aggregate_occurrence(session)

            self.__update_occurrence_status(session, occurrence)
