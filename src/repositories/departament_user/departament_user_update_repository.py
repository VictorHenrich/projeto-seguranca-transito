from dataclasses import dataclass

from patterns.repository import BaseRepository, IFindRepository
from models import UsuarioDepartamento, Departamento
from .departament_user_find_repository import (
    DepartamentUserFindRepository,
    DepartamentUserFindRepositoryParams,
)


@dataclass
class DepartamentUserUpdateRepositoryParam:
    uuid_departament_user: str
    departament: Departamento
    name: str
    access: str
    password: str
    position: str


@dataclass
class DepartamentUserFindProps:
    uuid_departament_user: str
    departament: Departamento


class DepartamentUserUpdateRepository(BaseRepository):
    def update(self, params: DepartamentUserUpdateRepositoryParam) -> None:
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

        user_departament.nome = params.name
        user_departament.acesso = params.access
        user_departament.senha = params.password
        user_departament.cargo = params.position

        self.session.add(user_departament)
