from dataclasses import dataclass


from start import app
from patterns.repository import ICreateRepository
from patterns.service import IService
from models import User, Departament
from services.departament import DepartamentGettingUUIDService
from repositories.occurrence import (
    OccurrenceCreateRepository,
    OccurrenceCreateRepositoryParam,
)


@dataclass
class DepartamentCreateProps:
    user: User
    departament: Departament
    description: str
    obs: str


class OccurrenceCreationService:
    def execute(
        self, user: User, uuid_departament: str, description: str, obs: str
    ) -> None:

        with app.databases.create_session() as session:
            departament_getting_service: IService[
                Departament
            ] = DepartamentGettingUUIDService()

            departament: Departament = departament_getting_service.execute(
                uuid_departament=uuid_departament
            )

            occurrence_creation_repo_param: OccurrenceCreateRepositoryParam = (
                DepartamentCreateProps(
                    user=user, departament=departament, description=description, obs=obs
                )
            )

            occurrence_creation_repository: ICreateRepository[
                OccurrenceCreateRepositoryParam
            ] = OccurrenceCreateRepository(session)

            occurrence_creation_repository.create(occurrence_creation_repo_param)

            session.commit()
