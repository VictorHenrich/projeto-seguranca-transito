from typing import Any, Mapping, Optional, Union, TypeAlias, IO, Collection
from flask import Response
from abc import ABC
import json
from datetime import datetime, date, timedelta
from io import IOBase
import mimetypes
from pathlib import Path


FileContent: TypeAlias = Union[str, bytes, IO]
FileCollection: TypeAlias = Collection[Union[str, bytes]]
FileName: TypeAlias = Union[str, Path]


class ResponseDefaultEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, (datetime, date, timedelta)):
            return str(o)

        return super().default(o)


class ResponseDefaultJSON(ABC, Response):
    __header_default: Mapping[str, str] = {"Content-Type": "application/json"}

    def __init__(
        self,
        status_code: int,
        message: str,
        data: Optional[Any],
        header: Optional[Mapping[str, str]] = None,
    ) -> None:
        response_data: Mapping[str, Any] = {
            "status": status_code,
            "message": message,
        }

        if data is not None:
            response_data["result"] = data

        header_: Mapping[str, str] = {
            **ResponseDefaultJSON.__header_default,
            **(header or {}),
        }

        super().__init__(
            json.dumps(response_data, cls=ResponseDefaultEncoder), status_code, header_
        )


class ResponseSuccess(ResponseDefaultJSON):
    def __init__(
        self,
        status_code: int = 200,
        message: str = "OK",
        data: Optional[Any] = None,
        header: Optional[Mapping[str, str]] = None,
    ) -> None:
        super().__init__(status_code, message, data, header)


class ResponseFailure(ResponseDefaultJSON):
    def __init__(
        self,
        status_code: int = 500,
        message: str = "ERROR",
        data: Optional[Any] = None,
        header: Optional[Mapping[str, str]] = None,
    ) -> None:
        super().__init__(status_code, message, data, header)


class ResponseNotFound(ResponseDefaultJSON):
    def __init__(
        self,
        status_code: int = 404,
        message: str = "NOT FOUND",
        data: Optional[Any] = None,
        header: Optional[Mapping[str, str]] = None,
    ) -> None:
        super().__init__(status_code, message, data, header)


class ResponseInauthorized(ResponseDefaultJSON):
    def __init__(
        self,
        status_code: int = 401,
        message: str = "INAUTHORIZED",
        data: Optional[Any] = None,
        header: Optional[Mapping[str, str]] = None,
    ) -> None:
        super().__init__(status_code, message, data, header)


class ResponseIO(Response):
    def __init__(
        self,
        filename: FileName,
        file_content: FileContent,
        status_code: int = 200,
        header: Mapping[str, str] | None = None,
    ) -> None:
        response: Union[str, bytes, FileCollection] = self.__get_file_content(
            file_content
        )

        file_type: str = self.__get_file_type(filename)

        headers = {
            "Content-Type": file_type,
            "Content-Disposition": f"attachment; filename='{filename}'",
            **(header or {}),
        }

        super().__init__(response, status_code, headers)

    def __get_file_content(
        self, file_content: FileContent
    ) -> Union[str, bytes, FileCollection]:
        if isinstance(file_content, IOBase):
            return self.__handle_io(file_content)

        elif isinstance(file_content, (str, bytes)):
            return file_content

        else:
            raise Exception("Tipo de conteúdo do arquivo é inválido para a resposta!")

    def __handle_io(self, file_content: IO) -> FileCollection:
        if not file_content.readable():
            raise Exception("Conteudo de arquivo IO não é do tipo Readable!")

        file_content.seek(0)

        return file_content.readlines()

    def __get_file_type(self, filename: FileName) -> str:
        try:
            return mimetypes.guess_type(filename)[0]

        except IndexError:
            return "application/octet-stream"
