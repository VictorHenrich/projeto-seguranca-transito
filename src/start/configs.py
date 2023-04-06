from server.utils import UtilsEnv


env_value = UtilsEnv.get_values()


CLI = {
    "name": "CLI PROJETO SEGURANÇA",
    "description": "Sistema CLI resposável pela execução de linhas de comando para tarefas distintas",
    "version": 1.0,
    "managers": ["api", "websocket", "database"],
}

DATABASE = {
    "main": {
        "dialect": env_value["DB_DIALECT"],
        "host": env_value["DB_HOST"],
        "port": env_value["DB_PORT"],
        "dbname": env_value["DB_NAME"],
        "username": env_value["DB_USERNAME"],
        "password": env_value["DB_PASSWORD"],
        "debug": False,
        "driver": env_value["DB_DRIVER"]
    }
}


HTTP = {
    "host": env_value["HTTP_HOST"],
    "port": env_value["HTTP_PORT"],
    "secret_key": env_value["APP_KEY"],
    "debug": True,
}


WEBSOCKET = {
    "host": env_value["SOCKET_HOST"],
    "port": env_value["SOCKET_PORT"],
    "secret_key": env_value["APP_KEY"],
    "debug": True,
}
