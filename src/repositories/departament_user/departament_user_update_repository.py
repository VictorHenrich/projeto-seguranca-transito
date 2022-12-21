from dataclasses import dataclass

from patterns.repository import BaseRepository, IGettingRepository
from models import UsuarioDepartamento, Departamento
from .departament_user_getting_repository import (
    DepartamentUserGettingRepository,
    DepartamentUserGettingRepositoryParam
)



@dataclass
class DepartamentUserUpdateRepositoryParam:
    uuid_departament_user: str
    departament: Departamento
    name: str
    access: str
    password: str
    position: str



class DepartamentUserUpdateRepository(BaseRepository):
    def update(self, param: DepartamentUserUpdateRepositoryParam) -> None:
        with self.database.create_session() as session:
            getting_repository: IGettingRepository[DepartamentUserGettingRepositoryParam, UsuarioDepartamento] = \
                DepartamentUserGettingRepository(self.database)

            getting_repository_param: DepartamentUserGettingRepositoryParam = \
                DepartamentUserGettingRepositoryParam(
                    uuid_departament_user=param.uuid_departament_user,
                    departament=param.departament
                )

            user_departament: UsuarioDepartamento = getting_repository.get(getting_repository_param)

            user_departament.nome = param.name
            user_departament.acesso = param.access
            user_departament.senha = param.password
            user_departament.cargo = param.position

            session.add(user_departament)
            session.commit()