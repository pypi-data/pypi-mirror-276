from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from httpx import Response
    from .config import Config

import httpx
from devgoldyutils import LoggerAdapter, Colours

from . import errors
from .logger import mov_cli_logger
from .utils import hide_ip

__all__ = ("HTTPClient",)

class SiteMaybeBlocked(errors.MovCliException):
    """Raises there's a connection error during a get request."""
    def __init__(self, url: str, error: httpx.ConnectError) -> None:
        super().__init__(
            f"A connection error occurred while making a GET request to '{url}'.\n" \
            "There's most likely nothing wrong with mov-cli. Your ISP's DNS could be blocking this site or perhaps the site is down. " \
            f"{Colours.GREEN}SOLUTION: Use a VPN or switch DNS!{Colours.RED}\n" \
            f"Actual Error >> {error}"
        )

class HTTPClient():
    def __init__(self, config: Config) -> None:
        """A base class for building scrapers from."""
        self.config = config
        self.logger = LoggerAdapter(mov_cli_logger, prefix = self.__class__.__name__)

        self.__httpx_client = httpx.Client(
            timeout = config.http_timeout, 
            cookies = None
        )
        
        super().__init__()

    def get(
        self, 
        url: str, 
        headers: dict = {}, 
        include_default_headers: bool = True, 
        redirect: bool = False, 
        **kwargs
    ) -> Response:
        """Performs a GET request and returns httpx.Response."""
        self.logger.debug(Colours.GREEN.apply("GET") + f" -> {hide_ip(url, self.config)}")

        if include_default_headers is True:
            if headers.get("Referer") is None:
                headers.update({"Referer": url})
                
            headers.update(self.config.http_headers)

        try:
            response = self.__httpx_client.get(
                url, 
                headers = headers, 
                follow_redirects = redirect, 
                **kwargs
            )

            if response.is_error:
                self.logger.debug(
                    f"GET Request to '{response.url}' {Colours.RED.apply('failed!')} ({response})"
                )

            return response

        except httpx.ConnectError as e:
            # TODO: I think this needs improving. I see people are getting certificate errors that aren't being caught here.
            if "[SSL: CERTIFICATE_VERIFY_FAILED]" in str(e):
                raise SiteMaybeBlocked(url, e)

            raise e

    def post(
        self, 
        url: str,
        data: dict = {},
        json: dict = {}, 
        headers: dict = {}, 
        include_default_headers: bool = True, 
        redirect: bool = False, 
        **kwargs
    ) -> Response:
        """Performs a POST request and returns httpx.Response."""
        self.logger.debug(Colours.GREEN.apply("POST") + f" -> {hide_ip(url, self.config)}")

        if include_default_headers is True:
            if headers.get("Referer") is None:
                headers.update({"Referer": url})

            headers.update(self.config.http_headers)

        response = self.__httpx_client.post(
            url,
            data = data,
            json = json,
            headers = headers, 
            follow_redirects = redirect, 
            **kwargs
        )

        if response.is_error:
            self.logger.debug(
                f"POST Request to '{response.url}' failed! ({response})"
            )

        return response

    def set_cookies(self, cookies: dict) -> None:
        """Sets cookies."""
        self.__httpx_client.cookies = cookies