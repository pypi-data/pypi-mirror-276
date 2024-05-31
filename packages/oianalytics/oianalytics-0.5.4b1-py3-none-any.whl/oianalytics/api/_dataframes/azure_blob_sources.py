from typing import Optional

import pandas as pd

from .. import _credentials
from .. import endpoints
from .. import utils


__all__ = ["get_azure_blob_sources", "get_single_azure_blob_source"]


def get_azure_blob_sources(
    page: int = 0,
    page_size: int = 20,
    get_all_pages: bool = True,
    multithread_pages: bool = True,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> pd.DataFrame:
    """
    List azure blob sources configured in OIAnalytics.

    Parameters
    ----------
    page : int, default 0
        The page to retrieve. It is ignored if 'get_all_pages' is set to True.
    page_size : int, default 20.
        The size of a page. It is ignored if 'get_all_pages' is set to True.
    get_all_pages : bool, default True
        Whether to get all pages at once.
        If the value is set to True, the 'page' and 'page_size' arguments will be ignored, and the function will retrieve all pages.
    multithread_pages : bool, default True
        Only used when getting all pages. If True, pages are retrieved in multiple threads simultaneously.
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    pd.DataFrame
        A pandas DataFrame containing the details of all the azure blob sources, indexed by their IDs.

    """

    if get_all_pages:
        page = 0
        page_size = 500

    def get_page(page_num: int):
        return endpoints.azure_blob_sources.get_azure_blob_sources(
            page=page_num,
            page_size=page_size,
            api_credentials=api_credentials,
        )

    def parse_page(page_response: dict):
        page_df = pd.DataFrame(page_response["content"])
        # Expected columns if content is empty
        if page_df.shape[0] == 0:
            page_df = pd.DataFrame(
                columns=[
                    "id",
                    "tagContext",
                    "enabled",
                    "name",
                    "pollingRate",
                    "minAge",
                    "maxAge",
                    "regexPattern",
                    "container",
                    "accountName",
                    "customEndpoint",
                    "path",
                    "preserveFiles",
                    "containerNamePrepended",
                    "includeSubdirectories",
                ]
            )
        # Set index
        page_df.set_index("id", inplace=True)
        return page_df

        # Query endpoint

    df = utils.concat_pages_to_dataframe(
        getter=get_page,
        parser=parse_page,
        page=page,
        get_all_pages=get_all_pages,
        multithread_pages=multithread_pages,
    )

    # Output
    return df


def get_single_azure_blob_source(
    azure_blob_source_id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> pd.Series:
    """
    Get a specific azure blob source configured in OIAnalytics by its ID.

    Parameters
    ----------
    azure_blob_source_id : str
        The OIAnalytics ID of the azure blob polling source to retrieve.
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    pd.Series
        A pandas Series object that stores the details of a specific azure blob sourced.

    """
    # get response from the endpoint as a dictionary
    response = endpoints.azure_blob_sources.get_single_azure_blob_source(
        azure_blob_source_id=azure_blob_source_id, api_credentials=api_credentials
    )
    # build a pandas Series with the dictionary
    ser = pd.Series(response, dtype=object)

    # Output
    return ser
