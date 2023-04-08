from dataclasses import dataclass


from server import App
from patterns.repository import ICreateRepository
from patterns.service import IService
from models import User, Departament
from services.departament import (
    DepartamentFindingUUIDService,
    DepartamentFindingUUIDServiceProps,
)
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


@dataclass
class OccurrenceCreationServiceProps:
    user: User
    uuid_departament: str
    description: str
    obs: str


class OccurrenceCreationService:
    def execute(self, props: OccurrenceCreationServiceProps) -> None:
        with App.databases.create_session() as session:
            departament_getting_service: IService[
                DepartamentFindingUUIDServiceProps, Departament
            ] = DepartamentFindingUUIDService()

            departament_getting_service_props: DepartamentFindingUUIDServiceProps = (
                DepartamentFindingUUIDServiceProps(
                    uuid_departament=props.uuid_departament
                )
            )

            departament: Departament = departament_getting_service.execute(
                departament_getting_service_props
            )

            occurrence_creation_repo_param: OccurrenceCreateRepositoryParam = (
                DepartamentCreateProps(
                    user=props.user,
                    departament=departament,
                    description=props.description,
                    obs=props.obs,
                )
            )

            occurrence_creation_repository: ICreateRepository[
                OccurrenceCreateRepositoryParam, None
            ] = OccurrenceCreateRepository(session)

            occurrence_creation_repository.create(occurrence_creation_repo_param)

            session.commit()
