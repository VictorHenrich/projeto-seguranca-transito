from dotenv import dotenv_values, get_key
from pathlib import Path
from typing import Dict, Optional, Union, Any


EnvPathParameter = Optional[Union[str, Path]]
EnvReturn = Dict[str, Optional[str]]
EnvOptions = Dict[str, Any]


class FileEnvNotFoundError(FileNotFoundError):
    def __init__(self) -> None:
        super().__init__("Não possível localizar o arquivo .env!")


class UtilsEnv:
    __default_path: list[Path] = list(Path.cwd().glob("**/*.env"))

    @classmethod
    def __handle_path(cls, path: EnvPathParameter) -> Path:
        path_: Union[str, Path] = ([path] if path else cls.__default_path)[0]

        if not Path(path_).exists():
            raise FileEnvNotFoundError()

        return Path(path_)

    @classmethod
    def get_values(
        cls, path: EnvPathParameter = False, **options: EnvOptions
    ) -> EnvReturn:
        path_: Path = cls.__handle_path(path)

        return dotenv_values(path_, **options)

    @classmethod
    def get_value(
        cls, key: str, path: EnvPathParameter = False, **options: EnvOptions
    ) -> EnvReturn:
        path_: Path = cls.__default_path(path)

        return get_key(path_, key, **options)

    @classmethod
    def set_default_path(cls, path: Union[str, Path]) -> None:
        p: Path = Path(path)

        if not p.exists():
            raise FileEnvNotFoundError()

        cls.__default_path = p
