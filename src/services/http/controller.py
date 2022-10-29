from abc import ABC
from flask_restful import Resource
from flask import Response

from .responses_default import ResponseNotFound


class Controller(ABC, Resource):
    def get(self) -> Response:
        return ResponseNotFound()

    def post(self) -> Response:
        return ResponseNotFound()

    def delete(self) -> Response:
        return ResponseNotFound()

    def patch(self) -> Response:
        return ResponseNotFound()

    def put(self) -> Response:
        return ResponseNotFound()