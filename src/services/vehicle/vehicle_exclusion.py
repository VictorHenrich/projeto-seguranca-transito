from dataclasses import dataclass

from server.database import Databases
from models import User
from repositories.vehicle import VehicleDeleteRepository, VehicleDeleteRepositoryParams
from patterns.repository import IDeleteRepository


@dataclass
class VehicleDeleteProps:
    vehicle_uuid: str
    user: User


class VehicleExclusionService:
    def __init__(self, vehicle_uuid: str, user: User) -> None:
        self.__vehicle_delete_props: VehicleDeleteProps = VehicleDeleteProps(
            vehicle_uuid, user
        )

    def __delete(self) -> None:
        with Databases.create_session() as session:
            vehicle_delete_repo: IDeleteRepository[
                VehicleDeleteRepositoryParams, None
            ] = VehicleDeleteRepository(session)

            vehicle_delete_repo.delete(self.__vehicle_delete_props)

            session.commit()

    def execute(self) -> None:
        self.__delete()
