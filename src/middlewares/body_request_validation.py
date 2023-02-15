from typing import Type, TypeAlias, TypeVar, Mapping, Any
from flask import request
from server.http import Middleware, ResponseDefaultJSON, ResponseFailure


T = TypeVar("T")

JsonData: TypeAlias = Mapping[str, Any]
ParamsData: TypeAlias = Mapping[str, T]


class BodyRequestValidationMiddleware(Middleware):
    @classmethod
    def handle(cls, classe: Type[T]) -> ParamsData:
        dados_json: JsonData = request.get_json()

        dados_corpo: T = classe(**dados_json)

        return {"body_request": dados_corpo}

    @classmethod
    def catch(cls, exception: Exception) -> ResponseDefaultJSON:
        if TypeError:
            return ResponseFailure(data="Corpo da requisição é inválido!")

        raise exception
