from dataclasses import dataclass

from start import app
from patterns.repository import ICreateRepository
from models import Departamento
from repositories.departament_user import (
    DepartamentUserCreateRepository,
    DepartamentUserCreateRepositoryParam,
)


@dataclass
class DepartamentUserCreateProps:
    departament: Departamento
    name: str
    access: str
    password: str
    position: str


class DepartamentUserCriationService:
    def execute(
        self,
        departament: Departamento,
        name: str,
        user: str,
        password: str,
        position: str,
    ) -> None:
        with app.databases.create_session() as session:
            creating_repository_param: DepartamentUserCreateRepositoryParam = (
                DepartamentUserCreateProps(
                    departament=departament,
                    name=name,
                    access=user,
                    password=password,
                    position=position,
                )
            )

            creating_repository: ICreateRepository[
                DepartamentUserCreateRepositoryParam
            ] = DepartamentUserCreateRepository(session)

            creating_repository.create(creating_repository_param)

            session.commit()
