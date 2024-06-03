# Copyright 2024 Q-CTRL. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#    https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.

from __future__ import annotations

import os
from typing import Optional

from qctrlclient.auth import (
    BaseAuth,
    CliAuth,
)
from qctrlclient.client import (
    GraphQLClient,
    GraphQLClientError,
)
from qctrlcommons.utils import generate_user_agent

from .globals import global_value
from .utils import get_installed_version

_DEFAULT_API_URL = "https://federation-service.q-ctrl.com"
_DEFAULT_OIDC_URL = "https://id.q-ctrl.com"


def get_default_api_url() -> str:
    """
    Return the default API URL. Can be overridden by
    setting the `QCTRL_API_URL` environment variable.
    """
    return os.getenv("QCTRL_API_URL", _DEFAULT_API_URL)


def get_default_oidc_url() -> str:
    """
    Return the default OIDC URL. Can be overridden by
    setting the `QCTRL_OIDC_URL` environment variable.
    """
    return os.getenv("QCTRL_OIDC_URL", _DEFAULT_OIDC_URL)


@global_value("DEFAULT_CLI_AUTH")
def get_default_cli_auth() -> CliAuth:
    """
    Return default `CliAuth` object.
    """
    url = get_default_oidc_url()
    return CliAuth(url)


def get_authenticated_client_for_product(
    product_access_required: str,
    package_name: str,
    api_url: Optional[str] = None,
    auth: Optional[BaseAuth | str] = None,
    invalid_access_error_message: Optional[str] = None,
) -> GraphQLClient:
    """
    Return a `GraphQLClient` using default URL and Auth (if not provided)
    and check the user has the required access for CLI usage.

    Parameters
    ----------
    product_access_required : str
        The product access required for the user to use the CLI.
    package_name : str
        The package name to include in the User-Agent header.
    api_url : str, optional
        The API URL to use. If not provided, the default API URL will be used.
    auth : BaseAuth or str, optional
        The authentication object (or a URL as str to create one) to use.
        If not provided, the default authentication object will be used.
    invalid_access_error_message : str, optional
        The error message to show if the user does not have the required access.
    """

    if isinstance(auth, str):
        auth = CliAuth(auth)

    headers = {
        "User-Agent": generate_user_agent(
            package_name, get_installed_version(package_name)
        ),
    }
    client = GraphQLClient(
        url=api_url or get_default_oidc_url(),
        headers=headers,
        auth=auth or get_default_cli_auth(),
    )

    try:
        client.check_user_role(product_access_required)
    except GraphQLClientError as exc:
        raise RuntimeError(
            invalid_access_error_message
            or f"Invalid access for CLI usage, requires `{product_access_required}` access"
        ) from exc

    return client
