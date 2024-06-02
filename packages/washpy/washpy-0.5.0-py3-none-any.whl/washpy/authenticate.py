import re
from typing import Annotated, Tuple
import datetime
import json
from pydantic import AfterValidator, TypeAdapter, UrlConstraints
from pydantic_core import Url
import requests


def validate_device_url_path(url: "DeviceUrl") -> "DeviceUrl":
    """
    Validates, if the given `DeviceUrl` has the correct path, e.g. `/Devices/000116343328`.

    More specifically, the `Url` path must match this regex: `^/Devices/[0-9]{12}$`

    **raises**: `ValueError`, if the regex does not match
    """
    path_pattern = re.compile(r"^/Devices/[0-9]{12}$")
    if url.path is None or not path_pattern.match(url.path):
        raise ValueError(
            f"The URL Path is invalid. Given: {url}, expected sometthing like 'https://192.168.1.251/Devices/000116343328'"
        )
    return url


type DeviceUrl = Annotated[
    Url,
    UrlConstraints(allowed_schemes=["https"], host_required=True),
    AfterValidator(validate_device_url_path),
]
"""
A device url must be a valid https url with a given host,
and follow this scheme:

`https://<device_address>/Devices/<device_id>`

e.g. `'https://192.168.1.251/Devices/000116343328'`
"""


def parse_and_validate_device_url_to_str(url: str | DeviceUrl) -> str:
    """
    **raises**: `ValidationError`, if the given url is not a valid `DeviceUrl`
    """
    url_type_adapter = TypeAdapter(DeviceUrl)
    return str(url_type_adapter.validate_python(url))


class WrongCredentialsException(Exception):
    """
    Indicates, that a wrong user name or password has been given.
    """


class NoUserException(Exception):
    """
    Indicates, that no user exists on a given device.
    """


class LoginTimeoutException(Exception):
    """
    Indicates, that the login currently is in timeout state,
    and the user has to wait until any further login attempt.
    """


def authenticate(
    device_url: str | DeviceUrl,
    user: str,
    password: str,
    verify_https: bool | str = False,
    https_timeout: float = 3.05,
) -> Tuple[str, datetime.timedelta]:
    """
    `device_url`: e.g. `'https://192.168.1.251/Devices/000116343328'`

    `user`: e.g. `'MYUSER'`

    `password`: e.g. `'verySecurePassword!'`

    `verify_https`: is passed to the `requests.request` `verify` argument

    `https_timeout`: timeout for HTTPS connections, in seconds

    **returns**: a string, containing a bearer token, and a time duration for which the token is valid.
    If the token is used again within the valid time period, the valid time period is refreshed.

    **raises**:
      - `NoUserException`, if HTTP response code 401
      - `WrongCredentialsException`, if HTTP response code 403
      - `LoginTimeoutException`, if HTTP response code 429
      - `ValueError`, else, and not HTTP code 200
      - `ValidationError`, if the given url is not a valid `DeviceUrl`
    """
    device_url = parse_and_validate_device_url_to_str(device_url)
    url = device_url + "/profSession"

    payload = json.dumps({"LoginName": user, "Password": password})
    headers = {"Content-Type": "application/json"}

    response = requests.request(
        "POST",
        url,
        verify=verify_https,
        headers=headers,
        data=payload,
        timeout=https_timeout,
    )

    match response.status_code:
        case 200:
            # the happy case
            return (
                response.json()["SessionId"],
                datetime.timedelta(seconds=response.json()["Timeout"]),
            )
        case 401:
            raise NoUserException("No user has been created on this device")
        case 403:
            raise WrongCredentialsException(
                f"For the user {user}, the password {password} is wrong."
            )
        case 429:
            raise LoginTimeoutException(
                f"Too many bad login attempts have been made. Please wait."
            )
        case _:
            raise ValueError(f"Unable to authenticate: got HTTP response {response}")
