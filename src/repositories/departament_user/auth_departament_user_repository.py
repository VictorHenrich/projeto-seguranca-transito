from typing import Tuple

from start import app
from patterns import AuthRepository
from models import UsuarioDepartamento, Departamento
from exceptions import UserNotFoundError , DepartamentNotFoundError
from .interfaces import IUserDepartamentAuthorization



class AuthDepartamentUserRepository(AuthRepository[Tuple[Departamento, UsuarioDepartamento]]):
    def auth(self, login: IUserDepartamentAuthorization) -> Tuple[Departamento, UsuarioDepartamento]:
        with app.databases.create_session() as session:
            departament, user: Tuple[Departamento, UsuarioDepartamento] = \
                session\
                    .query(Departamento, UsuarioDepartamento)\
                    .join(Departamento, UsuarioDepartamento.id_departamento == Departamento.id)\
                    .filter(
                        UsuarioDepartamento.acesso == login.username,
                        UsuarioDepartamento.senha == login.password,
                        Departamento.id_uuid == login.uuid_departament
                    )\
                    .first()

            if not departament:
                raise DepartamentNotFoundError()

            if not user:
                raise UserNotFoundError()

            return departament, user
