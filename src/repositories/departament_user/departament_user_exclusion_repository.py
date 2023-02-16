from dataclasses import dataclass

from patterns.repository import BaseRepository, IFindRepository
from models import UsuarioDepartamento, Departamento
from .departament_user_find_repository import (
    DepartamentUserFindRepository,
    DepartamentUserFindRepositoryParams,
)


@dataclass
class DepartamentUserExclusionRepositoryParam:
    departament: str
    uuid_departament_user: str


@dataclass
class DepartamentUserFindProps:
    uuid_departament_user: str
    departament: Departamento


class DepartamentUserExclusionRepository(BaseRepository):
    def delete(self, params: DepartamentUserExclusionRepositoryParam) -> None:
        getting_repository: IFindRepository[
            DepartamentUserFindRepositoryParams, UsuarioDepartamento
        ] = DepartamentUserFindRepository(self.session)

        getting_repository_param: DepartamentUserFindRepositoryParams = (
            DepartamentUserFindProps(
                uuid_departament_user=params.uuid_departament_user,
                departament=params.departament,
            )
        )

        user_departament: UsuarioDepartamento = getting_repository.get(
            getting_repository_param
        )

        self.session.delete(user_departament)
