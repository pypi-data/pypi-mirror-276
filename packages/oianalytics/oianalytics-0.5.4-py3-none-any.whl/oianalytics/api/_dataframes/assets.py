from typing import Optional, List, Dict, Literal

import pandas as pd

from .. import _credentials
from .. import endpoints
from .. import utils

__all__ = [
    "get_asset_types",
    "get_single_asset_type",
    "get_assets",
    "get_single_asset",
    "update_single_asset_tags_and_values",
]


def get_asset_types(
    page: Optional[int] = None,
    name: Optional[str] = None,
    get_all_pages: bool = True,
    multithread_pages: bool = True,
    extract_from_tagcontext: Optional[str] = "value",
    expand_tagcontext: bool = True,
    extract_from_dataset: Optional[str] = "description",
    extract_from_staticdataset: Optional[str] = "description",
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    # Args validation
    if extract_from_tagcontext not in ["id", "value", None]:
        raise ValueError(
            f"Unexpected value for 'extract_from_tagcontext': {extract_from_tagcontext}"
        )

    if extract_from_tagcontext is None and expand_tagcontext is True:
        raise ValueError(
            "Tag context cannot be expanded if 'extract_from_tagcontext' is None"
        )

    if extract_from_dataset not in ["id", "name", "description", None]:
        raise ValueError(
            f"Unexpected value for 'extract_from_dataset': {extract_from_dataset}"
        )

    if extract_from_staticdataset not in ["id", "name", "description", None]:
        raise ValueError(
            f"Unexpected value for 'extract_from_staticdataset': {extract_from_staticdataset}"
        )

    # Init
    if get_all_pages is True:
        page = 0

    # Get credentials from environment if not provided
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    def get_page(page_num: int):
        page_response = endpoints.assets.get_asset_types(
            page=page_num, name=name, api_credentials=api_credentials
        )
        return page_response

    def parse_page(page_response: dict):
        page_df = pd.DataFrame(page_response["content"])

        # Expected columns if content is empty
        if page_df.shape[0] == 0:
            page_df = pd.DataFrame(columns=["id", "name"])

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

    # Format dataframe
    if extract_from_tagcontext == "value":
        df["tagContext"] = df["tagContext"].map(
            lambda tagcontext: {
                tag["tagKey"]["key"]: [
                    val["value"] for val in tag["accessibleTagValues"]
                ]
                for tag in tagcontext
            }
        )

    elif extract_from_tagcontext == "id":
        df["tagContext"] = df["tagContext"].map(
            lambda tagcontext: {
                tag["tagKey"]["id"]: [val["id"] for val in tag["accessibleTagValues"]]
                for tag in tagcontext
            }
        )

    if expand_tagcontext is True and extract_from_tagcontext is not None:
        df = utils.expand_dataframe_column(df, "tagContext", add_prefix=False)

    if extract_from_dataset is not None:
        df["dataSet"] = df["dataSet"].map(
            lambda dataset: [data[extract_from_dataset] for data in dataset]
        )

    if extract_from_staticdataset is not None:
        df["staticDataSet"] = df["staticDataSet"].map(
            lambda staticdataset: [
                data[extract_from_staticdataset] for data in staticdataset
            ]
        )

    # Output
    return df


def get_single_asset_type(
    asset_type_id: str,
    extract_from_dataset: Optional[
        Literal["id", "name", "description"]
    ] = "description",
    extract_from_tagcontext: Optional[Literal["id", "value"]] = "value",
    expand_tagcontext: bool = True,
    extract_from_staticdataset: Optional[
        Literal["id", "name", "description"]
    ] = "description",
    extract_from_pythonmodels: Optional[
        Literal["id", "name", "description"]
    ] = "description",
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> pd.Series:
    """
    Retrieve the details of a specific asset type with its ID.

    Parameters
    ----------
    asset_type_id : str
        The ID of the asset type to retrieve.
    extract_from_dataset : {'id', 'name', 'description'}, optional, default 'description'
        Key to be associated to the column 'dataSet'.
    extract_from_tagcontext : {'id', 'value'}, optional, default 'value'
        Key to be associated from the column 'tagContext'.
    expand_tagcontext : bool, default True
        Whether to expand the column 'tagContext'.
    extract_from_staticdataset : {'id', 'name', 'description}, optional, default 'description'
        Key to be associated to the column 'staticDataSet'.
    extract_from_pythonmodels : {'id', 'name', 'description}, optional, default 'description'
        Key to be associated to the column 'pythonModels'.
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    pd.Series
        A pandas Series containing the details of a specific asset type.
    """

    # Args validation
    if extract_from_tagcontext is None and expand_tagcontext is True:
        raise ValueError(
            "Tag context cannot be expanded if 'extract_from_tagcontext' is None"
        )

    # Get credentials from environment if not provided
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    response = endpoints.assets.get_single_asset_type(
        asset_type_id=asset_type_id, api_credentials=api_credentials
    )

    df = pd.DataFrame([response])
    df.set_index("id", inplace=True)

    # Format DataFrame
    if extract_from_dataset:
        df["dataSet"] = df["dataSet"].map(
            lambda dataset: [data[extract_from_dataset] for data in dataset]
        )

    if extract_from_tagcontext == "value":
        df["tagContext"] = df["tagContext"].map(
            lambda tagcontext: {
                tag["tagKey"]["key"]: [
                    val["value"] for val in tag["accessibleTagValues"]
                ]
                for tag in tagcontext
            }
        )
    elif extract_from_tagcontext == "id":
        df["tagContext"] = df["tagContext"].map(
            lambda tagcontext: {
                tag["tagKey"]["id"]: [val["id"] for val in tag["accessibleTagValues"]]
                for tag in tagcontext
            }
        )
    if expand_tagcontext is True and extract_from_tagcontext is not None:
        df = utils.expand_dataframe_column(df, "tagContext", add_prefix=False)

    if extract_from_staticdataset is not None:
        df["staticDataSet"] = df["staticDataSet"].map(
            lambda staticdataset: [
                data[extract_from_staticdataset] for data in staticdataset
            ]
        )

    if extract_from_pythonmodels is not None and extract_from_pythonmodels in [
        "id",
        "name",
    ]:
        df["pythonModels"] = df["pythonModels"].map(
            lambda pythonModels: [
                data[extract_from_pythonmodels] for data in pythonModels
            ]
        )
    elif extract_from_pythonmodels == "description":
        df["pythonModels"] = df["pythonModels"].map(
            lambda pythonModels: [
                data["pythonModel"]["description"] for data in pythonModels
            ]
        )

    ser = df.squeeze()

    # Output
    return ser


def get_assets(
    asset_type_id: str,
    tag_value_id: Optional[List[str]] = None,
    query: Optional[int] = None,
    page: Optional[int] = None,
    get_all_pages: bool = True,
    multithread_pages: bool = True,
    extract_from_assettype: Optional[str] = "name",
    extract_from_tags: Optional[str] = "value",
    expand_tags: bool = True,
    extract_from_staticdatavalues: Optional[str] = "description",
    expand_staticdatavalues: bool = True,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    # Args validation
    if extract_from_assettype not in ["id", "name", None]:
        raise ValueError(
            f"Unexpected value for 'extract_from_assettype': {extract_from_assettype}"
        )

    if extract_from_tags not in ["id", "value", None]:
        raise ValueError(
            f"Unexpected value for 'extract_from_tags': {extract_from_tags}"
        )

    if extract_from_tags is None and expand_tags is True:
        raise ValueError("Tags cannot be expanded if 'extract_from_tags' is None")

    if extract_from_staticdatavalues not in ["id", "name", "description", None]:
        raise ValueError(
            f"Unexpected value for 'extract_from_staticdatavalues': {extract_from_staticdatavalues}"
        )

    if extract_from_staticdatavalues is None and expand_staticdatavalues is True:
        raise ValueError(
            "Static data values cannot be expanded if 'extract_from_staticdatavalues' is None"
        )

    # Init
    if get_all_pages is True:
        page = 0

    # Get credentials from environment if not provided
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    def get_page(page_num: int):
        page_response = endpoints.assets.get_assets(
            asset_type_id=asset_type_id,
            tag_value_id=tag_value_id,
            query=query,
            page=page_num,
            api_credentials=api_credentials,
        )
        return page_response

    def parse_page(page_response: dict):
        page_df = pd.DataFrame(page_response["content"])

        # Expected columns if content is empty
        if page_df.shape[0] == 0:
            page_df = pd.DataFrame(columns=["id", "name", "description"])

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

    # Format dataframe
    if extract_from_assettype is not None:
        df["assetType"] = df["assetType"].map(
            lambda asset_type: asset_type[extract_from_assettype]
        )

    if extract_from_tags == "value":
        df["tags"] = df["tags"].map(
            lambda tags: {tag["tagKey"]["key"]: tag["value"] for tag in tags}
        )

    elif extract_from_tags == "id":
        df["tags"] = df["tags"].map(
            lambda tags: {tag["tagKey"]["id"]: tag["id"] for tag in tags}
        )

    if expand_tags is True and extract_from_tags is not None:
        df = utils.expand_dataframe_column(df, "tags", add_prefix=False)

    if extract_from_staticdatavalues is not None:
        df["staticDataValues"] = df["staticDataValues"].map(
            lambda sdv: {
                sd["assetTypeStaticData"][extract_from_staticdatavalues]: sd["value"]
                for sd in sdv
            }
        )

    if expand_staticdatavalues is True and extract_from_staticdatavalues is not None:
        df = utils.expand_dataframe_column(df, "staticDataValues", add_prefix=False)

    # Output
    return df


def get_single_asset(
    asset_id: str,
    extract_from_assettype: Optional[Literal["id", "name"]] = "name",
    extract_from_tags: Optional[Literal["id", "value"]] = "value",
    expand_tags: bool = True,
    extract_from_staticdatavalues: Optional[
        Literal["id", "name", "description"]
    ] = "description",
    expand_staticdatavalues: bool = True,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> pd.Series:
    """
    Retrieve the details of a specific asset with ots ID.

    Parameters
    ----------
    asset_id : str
        The ID of the asset to retrieve.
    extract_from_assettype : {'id', 'name'}, optional, default 'name'
        Key to be associated to the column 'assetType'.
    extract_from_tags : {'id', 'value'}, optional, default 'value'
        Key to be associated to the column 'tags'.
    expand_tags : bool, default True
        Whether to expand the column tags.
    extract_from_staticdatavalues : {'id', 'name', 'description'}, optional, default 'description'
        Key to be associated to the column 'staticDataValues'.
    expand_staticdatavalues : bool, default True
        Whether to expand the column 'staticDataValues'.
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    pd.Series
        A pandas Series containing the details of a specific asset type.
    """

    # Args validation
    if extract_from_tags is None and expand_tags is True:
        raise ValueError("Tags cannot be expanded if 'extract_from_tags' is None")

    if extract_from_staticdatavalues is None and expand_staticdatavalues is True:
        raise ValueError(
            "Static data values cannot be expanded if 'extract_from_staticdatavalues' is None"
        )

    # Get credentials from environment if not provided
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    response = endpoints.assets.get_single_asset(
        asset_id=asset_id, api_credentials=api_credentials
    )

    df = pd.DataFrame([response])
    df.set_index("id", inplace=True)

    # Format dataframe
    if extract_from_assettype is not None:
        df["assetType"] = df["assetType"].map(
            lambda asset_type: asset_type[extract_from_assettype]
        )

    if extract_from_tags == "value":
        df["tags"] = df["tags"].map(
            lambda tags: {tag["tagKey"]["key"]: tag["value"] for tag in tags}
        )

    elif extract_from_tags == "id":
        df["tags"] = df["tags"].map(
            lambda tags: {tag["tagKey"]["id"]: tag["id"] for tag in tags}
        )

    if expand_tags is True and extract_from_tags is not None:
        df = utils.expand_dataframe_column(df, "tags", add_prefix=False)

    if extract_from_staticdatavalues is not None:
        df["staticDataValues"] = df["staticDataValues"].map(
            lambda sdv: {
                sd["assetTypeStaticData"][extract_from_staticdatavalues]: sd["value"]
                for sd in sdv
            }
        )

    if expand_staticdatavalues is True and extract_from_staticdatavalues is not None:
        df = utils.expand_dataframe_column(df, "staticDataValues", add_prefix=False)

    ser = df.squeeze()

    # Output
    return ser


def update_single_asset_tags_and_values(
    asset_id: str,
    tag_values: Optional[Dict] = None,
    static_data_values: Optional[Dict] = None,
    static_data_units: Optional[Dict] = None,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    # Init
    if tag_values is None:
        tag_values = {}

    if static_data_values is None:
        static_data_values = {}

    if static_data_units is None:
        static_data_units = {}

    # Build payload
    tag_commands = []
    for tagkey_id, tagvalue in tag_values.items():
        tag_commands.append({"tagKeyId": tagkey_id, "id": None, "value": tagvalue})

    value_commands = []
    for data_id, value in static_data_values.items():
        value_commands.append(
            {
                "assetTypeStaticDataId": data_id,
                "value": value,
                "unitId": static_data_units.get(data_id),
            }
        )

    # Query endpoint
    response = endpoints.assets.update_single_asset_tags_and_values(
        asset_id=asset_id,
        tag_commands=tag_commands,
        value_commands=value_commands,
        api_credentials=api_credentials,
    )

    # Output
    return response
