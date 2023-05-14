from typing import Protocol, Optional
from datetime import date

from patterns.repository import IFindRepository, BaseRepository
from models import User
from .user_find_repository import UserFindRepository, UserFindRepositoryParams


class UserUpdateRepositoryParams(Protocol):
    user_uuid: str
    name: str
    email: str
    password: str
    document: str
    document_rg: str
    telephone: str
    state_issuer: str
    address_state: str
    address_city: str
    address_district: str
    address_street: str
    address_number: str
    birthday: date


class UserUpdateRepository(BaseRepository):
    def update(self, params: UserUpdateRepositoryParams) -> None:
        getting_repository: IFindRepository[
            UserFindRepositoryParams, User
        ] = UserFindRepository(self.session)

        user: User = getting_repository.find_one(params)

        user.cpf = params.document
        user.data_nascimento = params.birthday
        user.email = params.email
        user.nome = params.name
        user.senha = params.password
        user.telefone = params.telephone
        user.estado_emissor = params.state_issuer
        user.endereco_uf = params.address_state
        user.endereco_cidade = params.address_city
        user.endereco_bairro = params.address_district
        user.endereco_logradouro = params.address_street
        user.endereco_numero = params.address_number

        self.session.add(user)
