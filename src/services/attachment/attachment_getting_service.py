from typing import IO
from dataclasses import dataclass
from sqlalchemy.orm import Session
from io import BytesIO

from server.database import Databases
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

    def execute(self) -> IO:
        with Databases.create_session() as session:
            attachment: Attachment = self.__get_attanchment(session)

            if not attachment.caminho_interno:
                raise Exception("Não existe caminho para localizar o arquivo!")

            with open(attachment.caminho_interno, "rb") as file:
                new_file = BytesIO(file.read())

                new_file.name = file.name

                return new_file
