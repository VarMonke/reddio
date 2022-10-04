from typing import Optional, Union, Dict, Any

import aiohttp


class HTTPException(Exception):
    """Exception that is raised for HTTP request related failures
        Attributes
        -----------
        response: :class:`aiohttp.ClientResponse`
            The response of the failed HTTP request. This is an
            instance of :class:`aiohttp.ClientResponse`.

        text: :class:`str`
            The error text. This could be an empty string.

        status: :class:`int`
            The status code of the HTTP Request
        """

    __slots__ = ("response", "data", "status")

    def __init__(
        self,
        response: aiohttp.ClientResponse,
        data: Optional[Union[int, Dict[str, Any], aiohttp.StreamReader]],
    ):
        self.response  = response
        self.status = response.status

        if isinstance(data, dict):
            base_message = data.get("message", "No information found")
            self.text = base_message
        
        else:
            self.text = data

        fmt = f"{self.status}  {self.response.reason} (error code: {self.status}) {self.text}"

        super().__init__(fmt)


class NotFound(HTTPException):
    """Exception that's thrown when the status code 404 occurs.

        Subclass of :exc:`HTTPExcept
    """
    pass
