from typing import Optional
from dataclasses import dataclass
from pathlib import Path
from sqlalchemy.orm import Session

from server.database import Databases
from models import Attachment


@dataclass
class AttachmentFindProps:
    attachment_uuid: str


class AttachmentExclusionService:
    def __init__(
        self, attachment: Attachment, session: Optional[Session] = None
    ) -> None:
        self.__attachment: Attachment = attachment
        self.__session: Optional[Session] = session

    def __remove_file(self):
        if not self.__attachment.caminho_interno:
            raise Exception("Não existe caminho para localizar o arquivo!")

        file_path: Path = Path(self.__attachment.caminho_interno)

        if not file_path.exists():
            raise Exception("Arquivo não existe!")

        file_path.unlink()

    def __delete_attachment(self, session: Session) -> None:
        self.__remove_file()

        session.delete(self.__attachment)

    def execute(self) -> None:
        if self.__session:
            self.__delete_attachment(self.__session)

        else:
            with Databases.create_session() as session:
                self.__delete_attachment(session)

                session.commit()
