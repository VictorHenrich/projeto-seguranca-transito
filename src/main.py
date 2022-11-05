from start import server


@server.initialize
def start_http():
    import controllers

    server.http.start_app()


server.start()
