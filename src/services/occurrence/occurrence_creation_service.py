from dataclasses import dataclass


from server import App
from patterns.repository import ICreateRepository
from models import User
from repositories.occurrence import (
    OccurrenceCreateRepository,
    OccurrenceCreateRepositoryParam,
)


@dataclass
class OccurrenceCreationServiceProps:
    user: User
    uuid_departament: str
    description: str
    code_external: str
    obs: str


class OccurrenceCreationService:
    def execute(self, props: OccurrenceCreationServiceProps) -> None:
        with App.databases.create_session() as session:
            occurrence_creation_repository: ICreateRepository[
                OccurrenceCreateRepositoryParam, None
            ] = OccurrenceCreateRepository(session)

            occurrence_creation_repository.create(props)

            session.commit()
