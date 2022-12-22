from datetime import datetime, timedelta

from start import app
from server.database import Database
from server.utils import UtilsJWT, Constants
from patterns.service import IService
from patterns.repository import IAuthRepository
from models import Departamento, UsuarioDepartamento
from repositories.departament_user import (
    DepartamentUserAuthRepositoryParam,
    DepartamentUserAuthRepository
)
from services.departament import DepartamentGettingService
from utils.entities import PayloadDepartamentUserJWT


class DepartamentUserAuthorizationService:
    def execute(
        self,
        departament_access: str,
        user: str,
        password: str
    ) -> str:
        database: Database = app.databases.get_database()

        dep_user_auth_repository_param: DepartamentUserAuthRepositoryParam = \
            DepartamentUserAuthRepositoryParam(
                departament_access=departament_access,
                user=user,
                password=password
            )

        dep_user_auth_repository: IAuthRepository[DepartamentUserAuthRepositoryParam, UsuarioDepartamento] = \
            DepartamentUserAuthRepository(database)

        
        departament_user: UsuarioDepartamento = dep_user_auth_repository.auth(dep_user_auth_repository_param)

        departament_getting_service: IService[Departamento] = DepartamentGettingService()

        departament: Departamento = departament_getting_service.execute(departament_user.id_departamento)

        expired: float = \
            (datetime.now() + timedelta(minutes=Constants.Authentication.max_minute_authenticated)).timestamp()

        payload: PayloadDepartamentUserJWT = PayloadDepartamentUserJWT(
            departament_user.id_uuid,
            departament.id_uuid,
            expired
        )

        token: str = UtilsJWT.encode(
            payload.__dict__, 
            app.http.application.secret_key
        )

        return f"Bearer {token}"