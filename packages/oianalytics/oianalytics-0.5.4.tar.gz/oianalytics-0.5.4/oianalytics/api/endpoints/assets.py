from typing import Optional, List, Dict

import requests

from .. import _credentials


__all__ = [
    "get_asset_types",
    "get_single_asset_type",
    "delete_asset_type",
    "get_assets",
    "get_single_asset",
    "update_single_asset_tags_and_values",
    "delete_asset",
]


def get_asset_types(
    page: Optional[int] = None,
    name: Optional[str] = None,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    # Get credentials from environment if not provided
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    # Query endpoint
    url = f"{api_credentials.base_url}/api/oianalytics/asset-types"
    response = requests.get(
        url=url,
        params={"page": page, "name": name},
        **api_credentials.auth_kwargs,
    )

    # Output
    response.raise_for_status()
    return response.json()


def get_single_asset_type(
    asset_type_id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> dict:
    # Get credentials from environment if not provided
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    # Query endpoint
    url = f"{api_credentials.base_url}/api/oianalytics/asset-types/{asset_type_id}"
    response = requests.get(
        url=url,
        **api_credentials.auth_kwargs,
    )

    # Output
    response.raise_for_status()
    return response.json()


def delete_asset_type(
    asset_type_id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> int:
    """
    Delete an asset type identified by its ID. The deletion will fail if the asset type is used somewhere in the system.

    Parameters
    ----------
    asset_type_id : str
        The OIAnalytics ID of the asset type to retrieve.
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
    url = f"{api_credentials.base_url}/api/oianalytics/asset-types/{asset_type_id}"
    response = requests.delete(
        url=url,
        **api_credentials.auth_kwargs,
    )

    response.raise_for_status()
    return response.status_code


def get_assets(
    asset_type_id: str,
    tag_value_id: Optional[List[str]] = None,
    query: Optional[int] = None,
    page: Optional[int] = None,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    # Get credentials from environment if not provided
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    # Query endpoint
    url = f"{api_credentials.base_url}/api/oianalytics/assets"
    response = requests.get(
        url=url,
        params={
            "page": page,
            "query": query,
            "assetTypeId": asset_type_id,
            "tagValueIds": tag_value_id,
        },
        **api_credentials.auth_kwargs,
    )

    # Output
    response.raise_for_status()
    return response.json()


def get_single_asset(
    asset_id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> dict:
    # Get credentials from environment if not provided
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    # Query endpoint
    url = f"{api_credentials.base_url}/api/oianalytics/assets/{asset_id}"
    response = requests.get(
        url=url,
        **api_credentials.auth_kwargs,
    )

    # Output
    response.raise_for_status()
    return response.json()


def update_single_asset_tags_and_values(
    asset_id: str,
    tag_commands: Optional[List[Dict]] = None,
    value_commands: Optional[List[Dict]] = None,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    # Get credentials from environment if not provided
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    # Init commands
    if tag_commands is None:
        tag_commands = []

    if value_commands is None:
        value_commands = []

    # Build payload
    payload = [
        {
            "assetId": asset_id,
            "tagCommands": tag_commands,
            "staticDataValueCommands": value_commands,
        }
    ]

    # Query endpoint
    url = f"{api_credentials.base_url}/api/oianalytics/assets/tags-and-values"
    response = requests.put(url=url, json=payload, **api_credentials.auth_kwargs)

    # Output
    response.raise_for_status()
    return response.status_code


def delete_asset(
    asset_id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> int:
    """
    Delete an asset identified by its id.

    Parameters
    ----------
    asset_id : str
        The OIAnalytics ID of the asset to be deleted.
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
    url = f"{api_credentials.base_url}/api/oianalytics/assets/{asset_id}"
    response = requests.delete(
        url=url,
        **api_credentials.auth_kwargs,
    )

    response.raise_for_status()
    return response.status_code
