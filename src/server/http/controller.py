from abc import ABC
from typing import TypeAlias, Sequence, Dict, Any
from flask_restful import Resource
from flask import Response
from .responses_default import ResponseNotFound


Args: TypeAlias = Sequence[Any]
Kwargs: TypeAlias = Dict[str, Any]


class Controller(Resource, ABC):
    def get(self, *args: Args, **kwargs: Kwargs) -> Response:
        return ResponseNotFound()

    def post(self, *args: Args, **kwargs: Kwargs) -> Response:
        return ResponseNotFound()

    def delete(self, *args: Args, **kwargs: Kwargs) -> Response:
        return ResponseNotFound()

    def patch(self, *args: Args, **kwargs: Kwargs) -> Response:
        return ResponseNotFound()

    def put(self, *args: Args, **kwargs: Kwargs) -> Response:
        return ResponseNotFound()
