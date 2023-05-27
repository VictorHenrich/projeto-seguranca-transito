from typing import Mapping, Any
from dataclasses import dataclass
from sqlalchemy.orm import Session

from server import App
from patterns.repository import IFindRepository
from repositories.attachment import (
    AttachmentFindRepository,
    AttachmentFindRepositoryParams,
)
from models import Attachment


@dataclass
class AttachmentFindProps:
    attachment_uuid: str


class AttachmentGettingService:
    def __init__(self, attachment_uuid: str) -> None:
        self.__props: AttachmentFindRepositoryParams = AttachmentFindProps(
            attachment_uuid
        )

    def __get_attanchment(self, session: Session) -> Attachment:
        attachment_find_repo: IFindRepository[
            AttachmentFindRepositoryParams, Attachment
        ] = AttachmentFindRepository(session)

        return attachment_find_repo.find_one(self.__props)

    def execute(self) -> Mapping[str, Any]:
        with App.databases.create_session() as session:
            attachment: Attachment = self.__get_attanchment(session)

            with open(attachment.caminho_interno) as file:
                return {"filename": file.name, "content": file.read()}
