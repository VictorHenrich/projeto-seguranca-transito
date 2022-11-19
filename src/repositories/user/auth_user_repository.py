from start import app
from patterns import AuthRepository
from exceptions import UserNotFoundError
from models import Usuario
from .interfaces import IUserAuthorization



class AuthUserRepository(AuthRepository[Usuario]):
    def auth(self, login: IUserAuthorization) -> Usuario:
        with app.databases.create_session() as session:
            user: Usuario = \
                session\
                    .query(Usuario)\
                    .filter(
                        Usuario.email == login.email,
                        Usuario.senha == login.password
                    )\
                    .first()

            if not user:
                raise UserNotFoundError()

            return user