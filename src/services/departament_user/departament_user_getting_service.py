from dataclasses import dataclass

from start import app
from patterns.repository import IFindRepository
from repositories.departament_user import (
    DepartamentUserFindRepository,
    DepartamentUserFindRepositoryParams,
)
from models import UsuarioDepartamento, Departamento


@dataclass
class DepartamentUserFindProps:
    uuid_departament_user: str
    departament: Departamento


class DepartamentUserGettingService:
    def execute(
        self, departament: Departamento, uuid_departament_user: UsuarioDepartamento
    ) -> UsuarioDepartamento:
        with app.databases.create_session() as session:
            getting_repository_param: DepartamentUserFindRepositoryParams = (
                DepartamentUserFindProps(
                    departament=departament, uuid_departament_user=uuid_departament_user
                )
            )

            getting_repository: IFindRepository[
                DepartamentUserFindRepositoryParams, UsuarioDepartamento
            ] = DepartamentUserFindRepository(session)

            user: UsuarioDepartamento = getting_repository.get(getting_repository_param)

            return user
