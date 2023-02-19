class FileEnvNotFoundError(FileNotFoundError):
    def __init__(self) -> None:
        super().__init__("Não possível localizar o arquivo .env!")
