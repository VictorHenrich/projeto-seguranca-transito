from start import app
from patterns.repository import IGettingRepository
from models import Departamento
from repositories.departament import (
    DepartamentGettingRepository,
    DepartamentGettingRepositoryParam
)


class DepartamentGettingService:
    def execute(
        self,
        departament_id: int
    ) -> Departamento:
        with app.databases.create_session() as session:
            getting_repository_param: DepartamentGettingRepositoryParam = \
                DepartamentGettingRepositoryParam(departament_id)

            getting_repository: IGettingRepository[DepartamentGettingRepositoryParam, Departamento] = \
                DepartamentGettingRepository(session)

            departament: Departamento = getting_repository.get(getting_repository_param)

            return departament