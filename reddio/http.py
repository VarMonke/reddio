from typing import Dict, Union, Optional
import platform

import aiohttp

from .constants import BASE_API_URL

from .exceptions import HTTPException, NotFound


class http:
    """The http class that handles requests"""

    def __init__(self, auth: Optional[aiohttp.BasicAuth] = None) -> None:
        self.auth = auth
        self.headers = {
            "User-Agent": ("Reddio (https://github.com/VarMonke/reddio)"
            f"Python/{platform.python_version()} aiohttp/{aiohttp.__version__}")
        }

    async def request(
        self,
        method: str,
        endpoint: str,
        *,
        params: Optional[Dict[str, Union[str, int]]] = None,
        data: Optional[Dict[str, Union[str, int]]] = None,
    ):
        if not hasattr(self, "session"):
            self.session = aiohttp.ClientSession(headers=self.headers, auth=self.auth)

        request_url = f"{BASE_API_URL}/{endpoint}"

        response = await self.session.request(
            method, request_url, headers=self.headers, params=params, json=data
        )

        try:
            data = await response.json()
        except aiohttp.client_exceptions.ContentTypeError:
            data = response.content

        remaining = self.headers.get("x-ratelimit-remaining")

        if 300 > response.status >= 200:
            return data
        elif response.status == 429 or remaining == "0":
            raise HTTPException(response, data)
        elif response.status == 404:
            raise NotFound(response, data)
