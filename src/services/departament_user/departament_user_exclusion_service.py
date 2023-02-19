from dataclasses import dataclass

from start import app
from patterns.repository import IDeleteRepository
from repositories.departament_user import (
    DepartamentUserDeleteRepository,
    DepartamentUserDeleteRepositoryParams,
)
from models import UsuarioDepartamento, Departamento


@dataclass
class DepartamentUserDeleteProps:
    epartament: str
    uuid_departament_user: str


class DepartamentUserExclusionService:
    def execute(
        self, departament: Departamento, uuid_departament_user: UsuarioDepartamento
    ) -> None:
        with app.databases.create_session() as session:
            exclusion_repository_param: DepartamentUserDeleteRepositoryParams = (
                DepartamentUserDeleteProps(
                    departament=departament, uuid_departament_user=uuid_departament_user
                )
            )

            exclusion_repository: IDeleteRepository[
                DepartamentUserDeleteRepositoryParams
            ] = DepartamentUserDeleteRepository(session)

            exclusion_repository.delete(exclusion_repository_param)

            session.commit()
