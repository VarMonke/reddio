from typing import Optional, Union, Dict, Any

import aiohttp


class HTTPException(Exception):
    """Exception that is raised for HTTP request related failures"""

    def __init__(
        self,
        response: aiohttp.ClientResponse,
        data: Optional[Union[str, Dict[str, Union[str, int]]]],
    ):
        self.response: aiohttp.ClientResponse = response
        self.status: int = response.status
        self.code: int
        self.text: str

        if isinstance(data, dict):
            self.code = data.get("code", 0)

            self.text = data.get("message", "")
        else:
            self.text = data or ""
            self.code = 0

        message = f"{self.response.status} {self.response.reason}: {self.code}"
        if len(self.text):
            message += f" {self.text}"

        super().__init__(message)


class NotFound(HTTPException):
    """HTTPException that is raised when the status code is 404"""

    pass
