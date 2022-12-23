from typing import List
from start import app
from patterns.repository import IListingRepository
from repositories.departament_user import (
    DepartamentUserListingRepository,
    DepartamentUserListingRepositoryParam
)
from models import UsuarioDepartamento, Departamento


class DepartamentUserListingService:
    def execute(
        self,
        departament: Departamento
    ) -> List[UsuarioDepartamento]:

        with app.databases.create_session() as session:
            listing_repository_param: DepartamentUserListingRepositoryParam = \
                DepartamentUserListingRepositoryParam(
                    departament=departament
                )

            listing_repository: IListingRepository[DepartamentUserListingRepositoryParam, UsuarioDepartamento] = \
                DepartamentUserListingRepository(session)

            users: List[UsuarioDepartamento] = listing_repository.list(listing_repository_param)

            return users