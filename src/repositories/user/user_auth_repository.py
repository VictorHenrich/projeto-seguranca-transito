from sqlalchemy.sql.functions import func
import logging

from typing import Protocol, Optional
from patterns.repository import BaseRepository
from models import User
from exceptions import UserNotFoundError


class UserAuthRepositoryParams(Protocol):
    email: str
    password: str

class UserAuthRepository(BaseRepository):
    def auth(self, params: UserAuthRepositoryParams) -> User:
        user: Optional[User] = (
            self.session.query(User)
            .filter(
                func.upper(User.email) == params.email.upper(), 
                User.senha == params.password
            )
            .first()
        )

        if not user:
            raise UserNotFoundError()
        
        logging.info(f"Usuário localizado: {user}")

        return user
