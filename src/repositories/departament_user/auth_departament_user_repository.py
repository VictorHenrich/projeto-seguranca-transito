from start import app
from patterns import AuthRepository
from models import UsuarioDepartamento
from exceptions import UserNotFoundError 
from .interfaces import AuthUserDepartament



class AuthDepartamentUserRepository(AuthRepository[UsuarioDepartamento]):
    def auth(self, login: AuthUserDepartament) -> UsuarioDepartamento:
        with app.databases.create_session() as session:
            user: UsuarioDepartamento = \
                session\
                    .query(UsuarioDepartamento)\
                    .filter(
                        UsuarioDepartamento.acesso == login.username,
                        UsuarioDepartamento.senha == login.password,
                        UsuarioDepartamento.id_departamento == login.departament.id
                    )

            if not user:
                raise UserNotFoundError()
