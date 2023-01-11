from start import app
from patterns.repository import IUpdateRepository
from repositories.departament_user import (
    DepartamentUserUpdateRepository,
    DepartamentUserUpdateRepositoryParam
)
from models import UsuarioDepartamento, Departamento


class DepartamentUserUpgradeService:
    def execute(
        self,
        departament: Departamento,
        uuid_departament_user: UsuarioDepartamento,
        name: str,
        user: str,
        password: str,
        position: str
    ) -> None:

        with app.databases.create_session() as session:
            update_repository_param: DepartamentUserUpdateRepositoryParam = \
                DepartamentUserUpdateRepositoryParam(
                    uuid_departament_user=uuid_departament_user,
                    departament=departament,
                    name=name,
                    access=user,
                    password=password,
                    position=position
                )

            update_repository: IUpdateRepository[DepartamentUserUpdateRepositoryParam] = \
                DepartamentUserUpdateRepository(session)

            update_repository.update(update_repository_param)

            session.commit()