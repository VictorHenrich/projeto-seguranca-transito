from abc import ABC
from typing import Any
from flask_restful import Resource
from flask import Response
from .responses_default import ResponseNotFound


class HttpController(Resource, ABC):
    def get(self, *args: Any, **kwargs: Any) -> Response:
        return ResponseNotFound()

    def post(self, *args: Any, **kwargs: Any) -> Response:
        return ResponseNotFound()

    def delete(self, *args: Any, **kwargs: Any) -> Response:
        return ResponseNotFound()

    def patch(self, *args: Any, **kwargs: Any) -> Response:
        return ResponseNotFound()

    def put(self, *args: Any, **kwargs: Any) -> Response:
        return ResponseNotFound()
