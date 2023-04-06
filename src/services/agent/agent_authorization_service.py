from dataclasses import dataclass
from datetime import datetime, timedelta

from server import App
from server.utils import UtilsJWT, Constants
from patterns.service import IService
from patterns.repository import IAuthRepository
from models import Departament, Agent
from repositories.agent import (
    AgentAuthRepositoryParam,
    AgentAuthRepository,
)
from services.departament import (
    DepartamentGettingService,
    DepartamentGettingServiceProps,
)
from utils.entities import PayloadDepartamentUserJWT


@dataclass
class AgentAuthorizationServiceProps:
    departament_access: str
    user: str
    password: str


class AgentAuthorizationService:
    def execute(self, props: AgentAuthorizationServiceProps) -> str:
        with App.databases().create_session() as session:
            dep_user_auth_repository: IAuthRepository[
                AgentAuthRepositoryParam, Agent
            ] = AgentAuthRepository(session)

            departament_user: Agent = dep_user_auth_repository.auth(props)

            departament_getting_service: IService[
                DepartamentGettingServiceProps, Departament
            ] = DepartamentGettingService()

            departament_getting_service_props: DepartamentGettingServiceProps = (
                DepartamentGettingServiceProps(departament_user.id_departamento)
            )

            departament: Departament = departament_getting_service.execute(
                departament_getting_service_props
            )

            expired: float = (
                datetime.now()
                + timedelta(minutes=Constants.Authentication.max_minute_authenticated)
            ).timestamp()

            payload: PayloadDepartamentUserJWT = PayloadDepartamentUserJWT(
                departament_user.id_uuid, departament.id_uuid, expired
            )

            token: str = UtilsJWT.encode(
                payload.__dict__, App.http().application.secret_key
            )

            return f"Bearer {token}"
