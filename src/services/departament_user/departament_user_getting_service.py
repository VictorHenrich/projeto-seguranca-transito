from start import app
from patterns.repository import IGettingRepository
from repositories.departament_user import (
    DepartamentUserGettingRepository,
    DepartamentUserGettingRepositoryParam
)
from models import UsuarioDepartamento, Departamento



class DepartamentUserGettingService:
    def execute(
        self,
        departament: Departamento,
        uuid_departament_user: UsuarioDepartamento
    ) -> UsuarioDepartamento:
        with app.databases.create_session() as session:
            getting_repository_param: DepartamentUserGettingRepositoryParam = \
                DepartamentUserGettingRepositoryParam(
                    departament=departament,
                    uuid_departament_user=uuid_departament_user
                )

            getting_repository: IGettingRepository[DepartamentUserGettingRepositoryParam, UsuarioDepartamento] = \
                DepartamentUserGettingRepository(session)

            user: UsuarioDepartamento = getting_repository.get(getting_repository_param)

            return user