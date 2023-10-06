from typing import Protocol
from datetime import date

from patterns.repository import BaseRepository
from models import User
from utils import CharUtils, BCryptUtils


class UserCreateRepositoryParams(Protocol):
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
    address_zipcode: str
    birthday: date


class UserCreateRepository(BaseRepository):
    def create(self, params: UserCreateRepositoryParams) -> User:
        user: User = User()

        user.rg = CharUtils.keep_only_number(params.document_rg)
        user.cpf = CharUtils.keep_only_number(params.document)
        user.data_nascimento = params.birthday
        user.email = params.email.upper()
        user.nome = params.name.upper()
        user.senha = BCryptUtils.generate_hash(params.password)
        user.telefone = CharUtils.keep_only_number(params.telephone)
        user.estado_emissor = params.state_issuer.upper()
        user.endereco_uf = params.address_state.upper()
        user.endereco_cidade = params.address_city.upper()
        user.endereco_bairro = params.address_district.upper()
        user.endereco_logradouro = params.address_street.upper()
        user.endereco_numero = CharUtils.keep_only_number(params.address_number)
        user.endereco_cep = CharUtils.keep_only_number(params.address_zipcode)

        self.session.add(user)
        self.session.flush()

        return user
