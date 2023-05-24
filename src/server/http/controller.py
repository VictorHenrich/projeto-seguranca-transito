from abc import ABC
from typing import TypeAlias, Collection, Mapping, Any
from flask_restful import Resource
from flask import Response
from .responses_default import ResponseNotFound


Args: TypeAlias = Collection[Any]
Kwargs: TypeAlias = Mapping[str, Any]


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
