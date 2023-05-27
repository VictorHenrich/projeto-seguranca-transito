from typing import IO
from uuid import UUID

from flask import Response
from server import App
from server.http import Controller, ResponseIO
from services.attachment import AttachmentGettingService
from patterns.service import IService

@App.http.add_controller(
    "/ocorrencia/anexos/<uuid:attachment_hash>"
)
class AttachmentController(Controller):
    def get(self, attachment_hash: UUID) -> Response:
        attachment_getting_service: IService[IO] = AttachmentGettingService(str(attachment_hash))

        file: IO = attachment_getting_service.execute()

        return ResponseIO(file.name, file)