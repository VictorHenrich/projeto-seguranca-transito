from services import Server, ServerFectory

from .configs import (
    DATABASES,
    HTTP,
    WEBSOCKET
)



server: Server = ServerFectory.create(HTTP, DATABASES, WEBSOCKET)

