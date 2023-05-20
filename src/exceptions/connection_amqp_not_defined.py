from .base_exception import BaseExceptionApplication


class ConnectionAMQPNotDefined(BaseExceptionApplication):
    def __init__(self) -> None:
        super().__init__(
            "Nenhuma conexão AMQP padrão foi estabelecida para inicialização!"
        )
