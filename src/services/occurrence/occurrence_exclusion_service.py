from typing import Collection
from dataclasses import dataclass
from sqlalchemy.orm import Session

from server import App, Databases
from patterns.repository import IFindRepository, IFindManyRepository
from patterns.service import IService
from repositories.occurrence import (
    OccurrenceFindRepository,
    OccurrenceFindRepositoryParams,
)
from repositories.attachment import (
    AttachmentFindManyRepository,
    AttachmentFindManyRepositoryParams,
)
from models import Occurrence, Attachment
from services.attachment import AttachmentExclusionService


@dataclass
class OccurrenceDeleteProps:
    occurrence_uuid: str


@dataclass
class AttachmentFindProps:
    occurrence: Occurrence


class OccurrenceExclusionService:
    def __init__(self, occurrence_uuid: str) -> None:
        self.__props: OccurrenceDeleteProps = OccurrenceDeleteProps(occurrence_uuid)

    def __get_occurrence(self, session: Session) -> Occurrence:
        occurrence_find_repo: IFindRepository[
            OccurrenceFindRepositoryParams, Occurrence
        ] = OccurrenceFindRepository(session)

        return occurrence_find_repo.find_one(self.__props)

    def __get_attachments(
        self, session: Session, occurrence: Occurrence
    ) -> Collection[Attachment]:
        attachments_find_many_repo: IFindManyRepository[
            AttachmentFindManyRepositoryParams, Attachment
        ] = AttachmentFindManyRepository(session)

        return attachments_find_many_repo.find_many(AttachmentFindProps(occurrence))

    def __delete_attachments(
        self, session: Session, attachments: Collection[Attachment]
    ) -> None:
        for attachment in attachments:
            attachment_exclusion_service: IService[None] = AttachmentExclusionService(
                attachment, session=session
            )

            attachment_exclusion_service.execute()

    def execute(self) -> None:
        with Databases.create_session() as session:
            occurrence: Occurrence = self.__get_occurrence(session)

            attachments: Collection[Attachment] = self.__get_attachments(
                session, occurrence
            )

            self.__delete_attachments(session, attachments)

            session.delete(occurrence)

            session.commit()
