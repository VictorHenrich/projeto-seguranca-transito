from typing import Type, TypeAlias, TypeVar, Mapping, Any
from dataclasses import dataclass

from server import App, HttpServer
from server.http import HttpMiddleware, ResponseDefaultJSON, ResponseFailure


T = TypeVar("T")

JsonData: TypeAlias = Mapping[str, Any]
ParamsData: TypeAlias = Mapping[str, T]


@dataclass
class BodyRequestValidationProps:
    cls: Type[Any]


class BodyRequestValidationMiddleware(HttpMiddleware[BodyRequestValidationProps]):
    def handle(self, props: BodyRequestValidationProps) -> ParamsData:
        dados_json: JsonData = HttpServer.global_request.get_json()

        dados_corpo: Any = props.cls(**dados_json)

        return {"body_request": dados_corpo}

    def catch(self, exception: Exception) -> ResponseDefaultJSON:
        if isinstance(exception, TypeError):
            return ResponseFailure(data="Corpo da requisição é inválido!")

        raise exception
