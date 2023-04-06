from dataclasses import dataclass

from server import App
from patterns.repository import ICreateRepository
from repositories.departament import (
    DepartamentCreateRepository,
    DepartamentCreateRepositoryParams,
)


@dataclass
class DepartamentCreationServiceProps:
    name: str
    unit: str
    access: str
    cep: str
    uf: str
    city: str
    district: str
    street: str
    complement: str


class DepartamentCreationService:
    def execute(self, props: DepartamentCreationServiceProps) -> None:
        with App.databases().create_session() as session:
            departament_create_repository: ICreateRepository[
                DepartamentCreateRepositoryParams, None
            ] = DepartamentCreateRepository(session)

            departament_create_repository.create(props)

            session.commit()
