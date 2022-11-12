


DATABASE = {
    "banco_principal":{
        "dialect": "postgresql",
        "host": "localhost",
        "port": "5432",
        "dbname": "banco_teste",
        "username": "postgres",
        "password": "1234",
        "debug": True,
        "async": False
    }
}


HTTP = {
    "host": "localhost",
    "port": 3333,
    "debug": True,
    "secret_key": "MINHA_CHAVE_SECRETA"
}


SOCKET = {
    "host": "localhost",
    "port": 5000,
    "debug": True
}