from dataclasses import dataclass

from start import app
from patterns.repository import IDeleteRepository
from repositories.user import UserDeleteRepository, UserDeleteRepositoryParams


@dataclass
class UserExclusionServiceProps:
    uuid_ser: str


class UserExclusionService:
    def execute(self, props: UserExclusionServiceProps) -> None:
        with app.databases.create_session() as session:
            repository: IDeleteRepository[
                UserDeleteRepositoryParams, None
            ] = UserDeleteRepository(session)

            repository.delete(props)

            session.commit()
