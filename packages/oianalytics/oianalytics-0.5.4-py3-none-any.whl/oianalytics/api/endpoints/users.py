from typing import Optional

import requests

from .. import _credentials


__all__ = ["get_users", "get_user_details", "delete_user"]


def get_users(
    page: Optional[int] = None,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    # Get credentials from environment if not provided
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    # Query endpoint
    url = f"{api_credentials.base_url}/api/oianalytics/users"
    response = requests.get(
        url=url,
        params={"page": page},
        **api_credentials.auth_kwargs,
    )

    # Output
    response.raise_for_status()
    return response.json()


def get_user_details(
    user_id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    # Get credentials from environment if not provided
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    # Query endpoint
    url = f"{api_credentials.base_url}/api/oianalytics/users/{user_id}"
    response = requests.get(
        url=url,
        **api_credentials.auth_kwargs,
    )

    # Output
    response.raise_for_status()
    return response.json()


def delete_user(
    user_id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> int:
    """
    Delete an existing user with a given id.

    Parameters
    ----------
    user_id : str
        The OIAnalytics ID of the user to delete.
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    int
        Status Code.
    """
    # Get credentials from environment if not provided
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    # Query endpoint
    url = f"{api_credentials.base_url}/api/oianalytics/users/{user_id}"
    response = requests.delete(
        url=url,
        **api_credentials.auth_kwargs,
    )

    response.raise_for_status()
    return response.status_code
