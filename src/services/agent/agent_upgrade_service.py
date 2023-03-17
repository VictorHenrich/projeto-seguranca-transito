from start import app
from patterns.repository import IUpdateRepository
from repositories.agent import (
    AgentUpdateRepository,
    AgentUpdateRepositoryParam,
)
from models import UsuarioDepartamento, Departamento


class AgentUpgradeService:
    def execute(
        self,
        departament: Departamento,
        uuid_departament_user: UsuarioDepartamento,
        name: str,
        user: str,
        password: str,
        position: str,
    ) -> None:

        with app.databases.create_session() as session:
            update_repository_param: AgentUpdateRepositoryParam = (
                AgentUpdateRepositoryParam(
                    uuid_departament_user=uuid_departament_user,
                    departament=departament,
                    name=name,
                    access=user,
                    password=password,
                    position=position,
                )
            )

            update_repository: IUpdateRepository[
                AgentUpdateRepositoryParam
            ] = AgentUpdateRepository(session)

            update_repository.update(update_repository_param)

            session.commit()
