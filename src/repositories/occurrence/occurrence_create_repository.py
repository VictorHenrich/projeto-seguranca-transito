from typing import Protocol
from datetime import datetime

from models import User, Occurrence, Vehicle
from patterns.repository import BaseRepository
from .occurrence_status import OccurrenceStatus


class OccurrenceCreateRepositoryParams(Protocol):
    user: User
    vehicle: Vehicle
    description: str
    address_state: str
    address_city: str
    address_district: str
    address_street: str
    address_number: str
    lat: str
    lon: str
    created: datetime = datetime.now()


class OccurrenceCreateRepository(BaseRepository):
    def create(self, params: OccurrenceCreateRepositoryParams) -> Occurrence:
        occurrence: Occurrence = Occurrence()

        occurrence.id_usuario = params.user.id
        occurrence.id_veiculo = params.vehicle.id
        occurrence.descricao = params.description
        occurrence.endereco_uf = params.address_state
        occurrence.endereco_cidade = params.address_city
        occurrence.endereco_bairro = params.address_district
        occurrence.endereco_logragouro = params.address_street
        occurrence.endereco_numero = params.address_number
        occurrence.latitude = params.lat
        occurrence.longitude = params.lon
        occurrence.data_cadastro = params.created
        occurrence.status = OccurrenceStatus.PROGRESS.value

        self.session.add(occurrence)
        self.session.flush()

        return occurrence
