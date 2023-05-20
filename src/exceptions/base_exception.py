import logging


class BaseExceptionApplication(Exception):
    def __init__(self, *messages) -> None:
        message: str = "".join(messages)

        super().__init__(message)
        
        logging.error(message)