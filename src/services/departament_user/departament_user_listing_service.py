from typing import List
from dataclasses import dataclass

from start import app
from patterns.repository import IFindManyRepository
from repositories.departament_user import (
    DepartamentUserFindManyRepository,
    DepartamentUserFindManyRepositoryParams,
)
from models import UsuarioDepartamento, Departamento


@dataclass
class DepartamentUserFindManyProps:
    departament: Departamento


class DepartamentUserListingService:
    def execute(self, departament: Departamento) -> List[UsuarioDepartamento]:

        with app.databases.create_session() as session:
            listing_repository_param: DepartamentUserFindManyRepositoryParams = (
                DepartamentUserFindManyProps(departament=departament)
            )

            listing_repository: IFindManyRepository[
                DepartamentUserFindManyRepositoryParams, UsuarioDepartamento
            ] = DepartamentUserFindManyRepository(session)

            users: List[UsuarioDepartamento] = listing_repository.list(
                listing_repository_param
            )

            return users
