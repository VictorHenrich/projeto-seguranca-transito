from start import server


@server.initialize
def start_http():
    import controllers
    import start.routes

    server\
        .http\
        .start_app()


#@server.initialize
def migrate():
    import models

    server\
        .databases\
        .get_database()\
        .migrate()




server.start()
