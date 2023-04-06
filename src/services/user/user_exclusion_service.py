from dataclasses import dataclass

from server import App
from patterns.repository import IDeleteRepository
from repositories.user import UserDeleteRepository, UserDeleteRepositoryParams


@dataclass
class UserExclusionServiceProps:
    uuid_ser: str


class UserExclusionService:
    def execute(self, props: UserExclusionServiceProps) -> None:
        with App.databases().create_session() as session:
            repository: IDeleteRepository[
                UserDeleteRepositoryParams, None
            ] = UserDeleteRepository(session)

            repository.delete(props)

            session.commit()
