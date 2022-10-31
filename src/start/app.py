from services import Server, ServerFectory

from .configs import (
    DATABASES,
    HTTP,
    WEBSOCKET
)



server: Server = ServerFectory.create(HTTP, DATABASES, WEBSOCKET)


@server.start
def run_app():
    from . import routes

    server.http.start_app()


server.start_server()

