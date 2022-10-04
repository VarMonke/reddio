from typing import Dict, Union, Optional
import platform

import aiohttp

from .exceptions import HTTPException, NotFound


class HTTPClient:
    """The http class that handles requests"""

    def __init__(self, auth: Optional[aiohttp.BasicAuth] = None) -> None:
        self.auth = auth
        self.headers = {
            "User-Agent": ("Reddio (https://github.com/VarMonke/reddio)"
            f"CPython/{platform.python_version()} aiohttp/{aiohttp.__version__}")
        }

    async def request(
        self,
        method: str,
        endpoint: str,
        *,
        params: Optional[Dict[str, Union[str, int]]] = None,
        data: Optional[Union[Dict[str, Union[str, int]], aiohttp.StreamReader]] = None,
    ):
        if not hasattr(self, "session"):
            self.session = aiohttp.ClientSession(headers=self.headers, auth=self.auth, base_url="https://api.reddit.com")

        response = await self.session.request(
            method, endpoint, headers=self.headers, params=params, json=data
        )

        try:
            data = await response.json()
        except aiohttp.client_exceptions.ContentTypeError: #type: ignore #I'm not sure why
            data = response.content

        remaining = self.headers.get("X-ratelimit-remaining")

        if 300 > response.status >= 200:
            return data

        if response.status == 429 or remaining == "0":
            raise HTTPException(response, data) 

        elif response.status == 404:
            raise NotFound(response, data)
