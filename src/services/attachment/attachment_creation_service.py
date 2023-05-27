from typing import Optional, Collection, Mapping, Any, Literal, TypeAlias
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4
from base64 import b64decode
from sqlalchemy.orm import Session
import mimetypes

from server import App
from patterns.repository import ICreateRepository
from repositories.attachment import (
    AttachmentCreateRepository,
    AttachmentCreateRepositoryParams,
)
from models import Occurrence


LiteralKeyAttachment: TypeAlias = Literal["content", "type"]


@dataclass
class AttachmentCreateProps:
    occurrence: Occurrence
    internal_path: Optional[str]
    url: Optional[str]


@dataclass
class AttachmentPayload:
    content: str
    type: str


class AttachmentCreationService:

    __INTERNAL_PATH: Path = Path.cwd() / "Objects" / "Occurrences"

    def __init__(
        self,
        occurrence: Occurrence,
        *attachments: Mapping[LiteralKeyAttachment, Any],
        url: Optional[str] = None,
    ) -> None:
        self.__occurrence: Occurrence = occurrence

        self.__url: Optional[str] = url

        self.__attachments: Collection[AttachmentPayload] = [
            AttachmentPayload(attachment["content"], attachment["type"])
            for attachment in attachments
        ]

    def __attach_file(self, attachment_payload: AttachmentPayload) -> str:
        extension: str = mimetypes.guess_extension(
            attachment_payload.type
        ) or mimetypes.guess_extension("application/octet-stream")

        if not AttachmentCreationService.__INTERNAL_PATH.exists():
            AttachmentCreationService.__INTERNAL_PATH.mkdir(parents=True)

        filename: str = str(
            AttachmentCreationService.__INTERNAL_PATH / f"{uuid4()}.{extension}"
        )

        filecontent: bytes = b64decode(attachment_payload.content)

        with open(filename, "wb") as file:
            file.write(filecontent)

        return filename

    def __create_attachment_in_database(
        self, session: Session, internal_path: str
    ) -> None:
        attachment_create_props: AttachmentCreateProps = AttachmentCreateProps(
            self.__occurrence, internal_path, self.__url
        )

        attachment_create_repo: ICreateRepository[
            AttachmentCreateRepositoryParams, None
        ] = AttachmentCreateRepository(session)

        attachment_create_repo.create(attachment_create_props)

    def execute(self) -> None:
        with App.databases.create_session() as session:
            for attachment in self.__attachments:
                internal_path: str = self.__attach_file(attachment)

                self.__create_attachment_in_database(session, internal_path)

                session.commit()
