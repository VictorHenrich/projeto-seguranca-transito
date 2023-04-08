from typing import Protocol

from patterns.repository import BaseRepository
from models import Departament


class DepartamentCreateRepositoryParams(Protocol):
    name: str
    unit: str
    access: str
    zipcode: str
    state: str
    city: str
    district: str
    street: str
    complement: str


class DepartamentCreateRepository(BaseRepository):
    def create(self, params: DepartamentCreateRepositoryParams) -> None:
        departament: Departament = Departament()

        departament.nome = params.name
        departament.acesso = params.access
        departament.cep = params.zipcode
        departament.uf = params.state
        departament.cidade = params.city
        departament.bairro = params.district
        departament.logradouro = params.street
        departament.complemento = params.complement
        departament.unidade = params.unit

        self.session.add(departament)
