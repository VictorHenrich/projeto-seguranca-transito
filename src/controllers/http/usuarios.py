from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from start import server
from services.http import (
    Controller,
    ResponseDefaultJSON,
    ResponseSuccess
)
from services.database import Database
from middleware import ValidacaoCorpoRequisicao, AutenticacaoUsuario
from models import Usuario
from exceptions import UserNotFoundError
from patterns.usuario.crud import (
    CadastroUsuario,
    DadosUsuario,
    VisualizacaoUsuario
)




db: Database = server.databases.get_database()


class UsuariosController(Controller):

    @ValidacaoCorpoRequisicao.apply(CadastroUsuario)
    def post(
        self,
        body_request: CadastroUsuario
    ) -> ResponseDefaultJSON:

        with db.create_session() as session:
            usuario: Usuario = Usuario()

            usuario.nome = body_request.nome
            usuario.email = body_request.email
            usuario.cpf = body_request.cpf
            usuario.senha = body_request.senha
            usuario.data_nascimento = body_request.data_nascimento

            session.add(usuario)

        return ResponseSuccess()


    @AutenticacaoUsuario.apply()
    @ValidacaoCorpoRequisicao.apply(CadastroUsuario)
    def put(
        self,
        auth: Usuario,
        hash_usuario: UUID,
        body_request: CadastroUsuario
    ) -> ResponseDefaultJSON:

        with db.create_session() as session:
            usuario: Usuario = \
                session\
                    .query(Usuario)\
                    .filter(Usuario.id_uuid == str(hash_usuario))\
                    .first()

            if not usuario:
                raise UserNotFoundError()

            usuario.email = body_request.email
            usuario.cpf = body_request.cpf
            usuario.data_nascimento = body_request.data_nascimento
            usuario.senha = body_request.senha

            session.add(usuario)

        return ResponseSuccess()


    @AutenticacaoUsuario.apply()
    def delete(
        self,
        hash_usuario: UUID,
        auth: Usuario
    ) -> ResponseDefaultJSON:
        with db.create_session() as session:
            usuario: Usuario = \
                session\
                    .query(Usuario)\
                    .filter(Usuario.id_uuid == str(hash_usuario))\
                    .first()

            if not usuario:
                raise UserNotFoundError()

            session.delete(usuario)
