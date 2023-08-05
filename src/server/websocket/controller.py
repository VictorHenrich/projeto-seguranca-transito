from typing import List, Generic, TypeVar, Optional
from abc import ABC, abstractmethod
from flask import request
from flask_socketio import Namespace


class ConnectionController:
    def __init__(self, id: str) -> None:
        self.__id = id

    @property
    def id(self) -> str:
        return self.__id


T = TypeVar("T", bound=ConnectionController)


class SocketController(Namespace, ABC, Generic[T]):
    def __init__(self, name: str) -> None:
        self.__connections: List[T] = []

        super().__init__(name)

    @property
    def connections(self) -> List[T]:
        return self.__connections

    def on_connect(self) -> None:
        connection: ConnectionController = ConnectionController(request.sid)

        connection_data: Optional[T] = self.on_open(connection)

        if connection_data:
            self.__connections.append(connection_data)

    def on_disconnect(self) -> None:
        for connection in self.__connections:
            if connection.id == request.sid:
                self.on_close(connection)

                self.__connections.remove(connection)

    @abstractmethod
    def on_open(self, connection: ConnectionController) -> Optional[T]:
        ...

    def on_close(self, connection: T) -> None:
        ...
