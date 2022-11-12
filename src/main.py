from start import server


@server.initialize
def start_http():
    import controllers
    import start.routes

    server.http.start_app()


server.start()
