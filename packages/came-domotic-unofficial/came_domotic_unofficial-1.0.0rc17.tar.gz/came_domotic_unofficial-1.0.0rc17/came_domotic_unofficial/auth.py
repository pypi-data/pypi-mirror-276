# Copyright 2024 - GitHub user: fredericks1982

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This module manages the HTTP interaction with the Came Domotic API.

Note:
   As a consumer of the CAME Domotic Unofficial library, **it's quite unlikely that you
   will need to use this class directly**: you should use the ``CameDomoticAPI`` and the
   CameEntity classes instead.

   In case of special needs, consider requesting the implementation of the desired
   feature in the Came Domotic Unofficial library, or forking the library and implement
   the feature yourself.
"""


import functools
import json
import time
from typing import Optional
import aiohttp
from asyncio import Lock

from cryptography.fernet import Fernet

from .errors import (
    CameDomoticAuthError,
    CameDomoticServerError,
    CameDomoticServerNotFoundError,
)


def handle_came_domotic_errors(func):
    """Decorator to handle CAME Domotic API errors.

    The decorator catches the following exceptions:
    - aiohttp.ClientResponseError: for HTTP errors (4xx, 5xx)
    - aiohttp.ClientError: for network-related errors
    - any other exception: for unforeseen errors

    Raises:
        CameDomoticAuthError: if an authentication error occurs.
        CameDomoticServerError: if a general error occurs.
    """

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except aiohttp.ClientResponseError as e:
            if e.status == 401:
                # Specific handling for authentication errors
                raise CameDomoticAuthError("Authentication failed") from e
            # General HTTP errors
            raise CameDomoticServerError(f"HTTP error {e.status}: {e.message}") from e
        except aiohttp.ClientError as e:
            # General network-related errors
            raise CameDomoticServerError("Network-related error") from e
        except Exception as e:
            # Catch-all for any other unforeseen errors
            raise CameDomoticServerError(
                "Generic error in communication with CAME Domotic API."
            ) from e

    return wrapper


class Auth:
    """Class to make authenticated requests to the CAME Domotic API server.

    Note:
        This class is not meant to be used directly, but through the ``CameDomoticAPI``
        class. To create an instance of this class, use the factory method
        ``async_create``.
    """

    # Default timeout "safe zone" for session expiration
    _DEFAULT_SAFE_ZONE_SEC = 30
    _DEFAULT_HTTP_HEADERS = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Connection": "Keep-Alive",
    }

    # Factory method to create an Auth instance
    @classmethod
    async def async_create(
        cls, websession: aiohttp.ClientSession, host: str, username: str, password: str
    ):
        """Create an Auth instance.

        Args:
            websession (ClientSession): the aiohttp client session.
            host (str): the host of the Came Domotic server.
            username (str): the username to use for the authentication.
            password (str): the password to use for the authentication.

        Returns:
            Auth: the Auth instance.
        """

        auth = cls(websession, host, username, password)
        await auth.async_validate_host()

        return auth

    @staticmethod
    def create_cypher_suite() -> Fernet:
        """Create a cypher suite."""
        key = Fernet.generate_key()
        return Fernet(key)

    def __init__(
        self, websession: aiohttp.ClientSession, host: str, username: str, password: str
    ):
        """Initialize the Auth instance.

        Args:
            websession (ClientSession): the aiohttp client session.
            host (str): the host of the Came Domotic server.
            username (str): the username to use for the authentication.
            password (str): the password to use for the authentication.

        Raises:
            CameDomoticServerNotFoundError: if the server is not available

        Note:
            The session is not logged in until the first request is made.
        """

        # Encrypt the username and password for security reasons:
        # the encryption key is generated at runtime and not stored anywhere.
        # This is not much secure, but it's better than storing the credentials
        # in clear text in the memory of the running process; also, this at least ensure
        # that the credentials cannot be written in the logs even by mistake.
        self.cipher_suite = Auth.create_cypher_suite()
        self.username = self.cipher_suite.encrypt(username.encode())
        self.password = self.cipher_suite.encrypt(password.encode())

        self.websession = websession
        self.host = host

        self.session_expiration_timestamp = (
            time.monotonic() - 3600
        )  # Set to an old timestamp to force login

        self.client_id = ""
        self.keep_alive_timeout_sec = 0
        self.cseq = 0

        self._lock = Lock()

    # region Context manager

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.async_dispose()

    # endregion

    def get_endpoint_url(self) -> str:
        """Get the CAME Domotic endpoint URL.

        Returns:
            str: the endpoint URL.
        """

        return f"http://{self.host}/domo/"

    @staticmethod
    def get_http_headers() -> dict:
        """Provide the default HTTP headers to use in the requests.

        Returns:
            dict: the HTTP headers.
        """

        return {
            "Content-Type": "application/json",  # "application/x-www-form-urlencoded",
            "Connection": "Keep-Alive",
        }

    async def async_get_valid_client_id(self) -> str:
        """Get a valid client ID, eventually logging in if needed.

        Returns:
            str: the client ID.

        Raises:
            CameDomoticAuthError: if an error occurs during the login.
        """

        if not self.validate_session():
            await self.async_login()
        return self.client_id

    @handle_came_domotic_errors
    async def async_send_command(
        self, payload: dict, timeout: Optional[int] = 10
    ) -> aiohttp.ClientResponse:
        """Send a command to the Came Domotic server.

        Args:
            payload (dict): the payload to send.
            timeout (int, optional): the timeout in seconds (default: 10s).

        Returns:
            ClientResponse: the response.

        Raises:
            CameDomoticServerError: if an error occurs during the command.
        """

        response = await self.websession.post(
            self.get_endpoint_url(),
            data={"command": json.dumps(payload)},
            headers=Auth._DEFAULT_HTTP_HEADERS,
            timeout=timeout,
        )

        # Check if the response HTTP status is 2xx
        if 200 <= response.status < 300:
            # Increment the command sequence number
            self.cseq += 1
            # Refresh the session expiration timestamp, keeping a "safe zone"
            self.session_expiration_timestamp = time.monotonic() + max(
                0, self.keep_alive_timeout_sec - Auth._DEFAULT_SAFE_ZONE_SEC
            )

        await self.async_raise_for_status_and_ack(response)

        return response

    # The following method is not async because it is used in the __init__ method
    async def async_validate_host(self, timeout: Optional[int] = 10) -> None:
        """Validate the host asynchronously using aiohttp.

        Args:
            timeout (int, optional): the timeout in seconds (default: 10s).

        Raises:
            CameDomoticServerNotFoundError: if an error occurs during the request.
        """
        try:
            async with self.websession.get(
                self.get_endpoint_url(), timeout=timeout
            ) as resp:
                # Ensure that the server URL is available
                resp.raise_for_status()
                if resp.status != 200:
                    raise aiohttp.ServerConnectionError(f"HTTP error {resp.status}.")

        except aiohttp.ClientResponseError as e:
            # Specific HTTP errors
            raise CameDomoticServerNotFoundError(
                f"HTTP error {e.status}: {e.message}"
            ) from e
        except aiohttp.ServerTimeoutError as e:
            # Handle timeouts specifically
            raise CameDomoticServerNotFoundError(
                "Timeout while trying to reach the server."
            ) from e
        except aiohttp.ClientError as e:
            # Broader category for client-side issues
            raise CameDomoticServerNotFoundError(
                f"Failed to reach server '{self.host}' due to client error."
            ) from e

    async def async_login(self) -> None:
        """Login to the Came Domotic server.

        Raises:
            CameDomoticAuthError: if an error occurs during the login.
        """
        async with self._lock:
            if not self.validate_session():
                payload = {
                    "sl_cmd": "sl_registration_req",
                    "sl_login": self.cipher_suite.decrypt(self.username).decode(),
                    "sl_pwd": self.cipher_suite.decrypt(self.password).decode(),
                }

                try:
                    response = await self.async_send_command(payload)
                    data = await response.json(content_type=None)
                    self.client_id = data.get("sl_client_id")
                    self.keep_alive_timeout_sec = data.get("sl_keep_alive_timeout_sec")
                except aiohttp.ClientResponseError as e:
                    if e.status == 401:
                        raise CameDomoticAuthError("Authentication failed") from e
                    raise CameDomoticAuthError("HTTP error during login") from e
                except Exception as e:
                    raise CameDomoticAuthError("Generic error logging in") from e

                self.session_expiration_timestamp = time.monotonic() + max(
                    0, self.keep_alive_timeout_sec - Auth._DEFAULT_SAFE_ZONE_SEC
                )

    async def async_keep_alive(self) -> None:
        """Keep the session alive, eventually logging in again if needed.

        Raises:
            CameDomoticServerError: if an error occurs during the keep-alive.
            CameDomoticAuthError: if an error occurs during the login.
        """
        async with self._lock:
            if not self.validate_session():
                await self.async_login()
            else:
                payload = {
                    "sl_client_id": self.client_id,
                    "sl_cmd": "sl_keep_alive_req",
                }
                await self.async_send_command(payload)

    @handle_came_domotic_errors
    async def async_logout(self) -> None:
        """Logout from the Came Domotic server.

        Raises:
            CameDomoticServerError: if an error occurs during the logout.
        """

        # Logout only if the session is still valid
        if self.validate_session():
            payload = {
                "sl_client_id": self.client_id,
                "sl_cmd": "sl_logout_req",
            }

            await self.async_send_command(payload)

            self.client_id = ""
            self.session_expiration_timestamp = time.monotonic()

    async def async_dispose(self):
        """Dispose the Auth instance, eventually logging out if needed."""
        if self.validate_session():
            try:
                await self.async_logout()
            except CameDomoticServerError:
                pass
        await self.websession.close()

    # region Utilities

    def validate_session(self) -> bool:
        """Check whether the session is still valid or not."""
        # Notice that self.session_expiration_timestamp already include the safe zone
        # set with the private constant _DEFAULT_SAFE_ZONE_SEC
        return (
            self.session_expiration_timestamp > time.monotonic()
            and self.client_id != ""
        )

    @staticmethod
    async def async_raise_for_status_and_ack(response: aiohttp.ClientResponse):
        """Check the response status and raise an error if necessary.

        Args:
            response (ClientResponse): the response.

        Raises:
            CameDomoticServerError: if there is an error interacting with
                the remote Came Domotic server.
        """
        try:
            response.raise_for_status()
        except Exception as e:
            raise CameDomoticServerError(
                f"Exception raised for HTTP status: {response.status}"
            ) from e

        try:
            resp_json = await response.json(content_type=None)
        except json.JSONDecodeError as e:
            raise CameDomoticServerError("Error decoding the response to JSON") from e

        ack_reason = resp_json.get("sl_data_ack_reason")

        if ack_reason and ack_reason != 0:
            raise CameDomoticServerError(f"Bad sl_data_ack_reason code: {ack_reason}")

    def backup_auth_credentials(self):
        """Backup the current authentication credentials."""
        return (
            self.username,
            self.password,
            self.client_id,
            self.session_expiration_timestamp,
            self.keep_alive_timeout_sec,
            self.cseq,
        )

    def restore_auth_credentials(self, backup_state):
        """Restore authentication credentials from a backup.

        Args:
            backup_state (tuple): Username and password.
        """
        (
            self.username,
            self.password,
            self.client_id,
            self.session_expiration_timestamp,
            self.keep_alive_timeout_sec,
            self.cseq,
        ) = backup_state

    def update_auth_credentials(self, username, password):
        """Update the authentication credentials.

        Args:
            username (str): New username.
            password (str): New password.
        """
        self.username = self.cipher_suite.encrypt(username.encode())
        self.password = self.cipher_suite.encrypt(password.encode())

        # Invalidate the (previous) session, since the credentials have changed
        self.session_expiration_timestamp = time.monotonic() - 3600
        self.client_id = ""

    # endregion
