from start.app import server


@server.start
def run_app():
    import start.routes

    server.http.start_app()


server.start_server()