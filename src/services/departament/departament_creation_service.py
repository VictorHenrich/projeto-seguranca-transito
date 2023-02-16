from dataclasses import dataclass

from start import app
from patterns.repository import ICreateRepository
from repositories.departament import (
    DepartamentCreateRepository,
    DepartamentCreateRepositoryParams,
)


@dataclass
class DepartamentCreateProps:
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
    def execute(
        self,
        name: str,
        unit: str,
        access: str,
        cep: str,
        uf: str,
        city: str,
        district: str,
        street: str,
        complement: str,
    ) -> None:

        with app.databases.create_session() as session:
            departament_create_props: DepartamentCreateRepositoryParams = (
                DepartamentCreateProps(
                    name, unit, access, cep, uf, city, district, street, complement
                )
            )

            departament_create_repository: ICreateRepository[
                DepartamentCreateRepositoryParams
            ] = DepartamentCreateRepository(session)

            departament_create_repository.create(departament_create_props)

            session.commit()