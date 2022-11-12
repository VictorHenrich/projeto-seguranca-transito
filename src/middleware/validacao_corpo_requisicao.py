from typing import Type, TypeAlias, TypeVar, Mapping, Any
from flask import request
from services.http import Middleware, ResponseDefaultJSON, ResponseFailure


T = TypeVar('T')

DadosJSON: TypeAlias = Mapping[str, Any]



class ValidacaoCorpoRequisicao(Middleware):
    @classmethod
    def handle(cls, classe: Type[T]):
        dados_json: DadosJSON = request.get_json()

        dados_corpo: T = classe(**dados_json)

        return {"body_request": dados_corpo}


    @classmethod
    def catch(cls, exception: Exception) -> ResponseDefaultJSON:
        return ResponseFailure(data="Corpo da requisição é inválido!")