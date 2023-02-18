from multiprocessing import Pool
from start import app


def migrate():
    import models

    app.databases.migrate(True)

    print("Migração feita com sucesso!")


def start_http():
    import controllers
    import start.routes

    app.http.run()


def start_websocket():
    import controllers

    app.websocket.run()
