from typing import Type, TypeAlias, TypeVar, Dict, Any
from dataclasses import dataclass

from server import App
from server.http import HttpMiddleware, ResponseDefaultJSON, ResponseFailure


T = TypeVar("T")

JsonData: TypeAlias = Dict[str, Any]
ParamsData: TypeAlias = Dict[str, T]


@dataclass
class BodyRequestValidationProps:
    class_: Type[Any]


class BodyRequestValidationMiddleware(HttpMiddleware[BodyRequestValidationProps]):
    def handle(self, props: BodyRequestValidationProps) -> ParamsData:
        dados_json: JsonData = App.http.global_request.get_json()

        dados_corpo: Any = props.class_(**dados_json)

        return {"body_request": dados_corpo}

    def catch(self, exception: Exception) -> ResponseDefaultJSON:
        if TypeError:
            return ResponseFailure(data="Corpo da requisição é inválido!")

        raise exception
