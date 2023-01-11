from dataclasses import dataclass

from patterns.repository import BaseRepository, IGettingRepository
from models import UsuarioDepartamento
from .departament_user_getting_repository import (
    DepartamentUserGettingRepository,
    DepartamentUserGettingRepositoryParam
)



@dataclass
class DepartamentUserExclusionRepositoryParam:
    departament: str
    uuid_departament_user: str


class DepartamentUserExclusionRepository(BaseRepository):
    def delete(self, param: DepartamentUserExclusionRepositoryParam) -> None:
        getting_repository: IGettingRepository[DepartamentUserGettingRepositoryParam, UsuarioDepartamento] = \
            DepartamentUserGettingRepository(self.session)

        getting_repository_param: DepartamentUserGettingRepositoryParam = \
            DepartamentUserGettingRepositoryParam(
                uuid_departament_user=param.uuid_departament_user,
                departament=param.departament
            )

        user_departament: UsuarioDepartamento = getting_repository.get(getting_repository_param)

        self.session.delete(user_departament)


