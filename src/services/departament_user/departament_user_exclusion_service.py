from start import app
from patterns.repository import IExclusionRepository
from repositories.departament_user import (
    DepartamentUserExclusionRepository,
    DepartamentUserExclusionRepositoryParam
)
from models import UsuarioDepartamento, Departamento


class DepartamentUserExclusionService:
    def execute(
        self,
        departament: Departamento,
        uuid_departament_user: UsuarioDepartamento
    ) -> None:
        with app.databases.create_session() as session:
            exclusion_repository_param: DepartamentUserExclusionRepositoryParam = \
                DepartamentUserExclusionRepositoryParam(
                    departament=departament,
                    uuid_departament_user=uuid_departament_user
                )

            exclusion_repository: IExclusionRepository[DepartamentUserExclusionRepositoryParam] = \
                DepartamentUserExclusionRepository(session)

            exclusion_repository.delete(exclusion_repository_param)

            session.commit()