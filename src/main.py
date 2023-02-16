from start import app


# @app.initialize
def migrate():
    import models

    app.databases.migrate(True)

    print("Migração feita com sucesso!")


@app.initialize
def start_http():
    import controllers
    import start.routes

    app.http.start_app()


if __name__ == "__main__":
    app.start()
