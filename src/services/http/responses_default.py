from typing import Any, Mapping, Optional
from flask import Response
from abc import ABC
import json



class ResponseDefaultJSON(ABC, Response):
    __header_default: Mapping[str, str] = {
        "Content-Type": "application/json"
    }

    def __init__(
        self,
        status_code: int,
        message: str,
        data: Optional[Any],
        header: Optional[Mapping[str, str]] = None
    ) -> None:
        response_data: Mapping[str, Any] = {
            "status": status_code,
            "message": message,
        }

        if data is not None:
            response_data['data'] = response_data

        header_: Mapping[str, str] = {**ResponseDefaultJSON.__header_default, **{header or {}}}

        super().__init__(json.dumps(response_data), status_code, header_)



class ResponseSuccess(ResponseDefaultJSON):
    def __init__(
        self, 
        status_code: int = 200, 
        message: str = "OK", 
        data: Optional[Any] = None, 
        header: Optional[Mapping[str, str]] = None
    ) -> None:
        super().__init__(status_code, message, data, header)



class ResponseFailure(ResponseDefaultJSON):
    def __init__(
        self, 
        status_code: int = 500, 
        message: str = "ERROR", 
        data: Optional[Any] = None, 
        header: Optional[Mapping[str, str]] = None
    ) -> None:
        super().__init__(status_code, message, data, header)



class ResponseNotFound(ResponseDefaultJSON):
    def __init__(
        self, 
        status_code: int = 404, 
        message: str = "NOT FOUND", 
        data: Optional[Any] = None, 
        header: Optional[Mapping[str, str]] = None
    ) -> None:
        super().__init__(status_code, message, data, header)



class ResponseInauthorized(ResponseDefaultJSON):
    def __init__(
        self, 
        status_code: int = 401, 
        message: str = "INAUTHORIZED", 
        data: Optional[Any] = None, 
        header: Optional[Mapping[str, str]] = None
    ) -> None:
        super().__init__(status_code, message, data, header)