

HTTP = {
    "host": "localhost",
    "port": 5000,
    "debug": True
}


WEBSOCKET = None


DATABASES = {
    "main":{
        "dialect": "postgresql",
        "host": "localhost",
        "port": "5432",
        "dbname": "teste",
        "user": "postgres",
        "password": "1234",
        "debug": True,
        "async": False
    }
}