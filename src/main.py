from start import app


@app.initialize
def start_http():
    import controllers
    import start.routes

    app\
        .http\
        .start_app()


#@app.initialize
def migrate():
    import models

    app\
        .databases\
        .get_database()\
        .migrate()




app.start()
