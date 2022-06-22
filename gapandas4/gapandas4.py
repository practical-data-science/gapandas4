"""
GAPandas4
"""

import os
import pandas as pd
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import MetricType
from google.analytics.data_v1beta.types import GetMetadataRequest


def _get_client(service_account):
    """Create a connection using a service account.

    Args:
        service_account (string): Filepath to Google Service Account client secrets JSON keyfile

    Returns:
        client (object): Google Analytics Data API client
    """

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = service_account
    client = BetaAnalyticsDataClient()

    return client


def _get_request(service_account, request):
    """Pass a request to the API and return a response.

    Args:
        service_account (string): Filepath to Google Service Account client secrets JSON keyfile

    Returns:
        response (object): Google Analytics Data API response
    """

    client = _get_client(service_account)
    response = client.run_report(request)
    return response


def _get_headers(response):
    """Return a Python list of dimension and metric header names from the Protobuf response.

    Args:
        response (object): Google Analytics Data API response

    Returns:
        headers (list): List of column header names.
    """

    headers = []

    for header in response.dimension_headers:
        headers.append(header.name)

    for header in response.metric_headers:
        headers.append(header.name)

    return headers


def _get_rows(response):
    """Return a Python list of row value lists from the Protobuf response.

    Args:
        response (object): Google Analytics Data API response

    Returns:
        rows (list): List of rows.

    """

    rows = []

    for _row in response.rows:

        row = []

        for dimension in _row.dimension_values:
            row.append(dimension.value)

        for metric in _row.metric_values:
            row.append(metric.value)

        rows.append(row)

    return rows


def _to_dataframe(response):
    """Returns a Pandas dataframe of results.

    Args:
        response (object): Google Analytics Data API response

    Returns:
        df (dataframe): Pandas dataframe created from response.
    """

    headers = _get_headers(response)
    rows = _get_rows(response)
    df = pd.DataFrame(rows, columns=headers)

    return df


def run_report(service_account, request):
    """Pass a Protobuf request to the GA4 API using runReport and return a Pandas dataframe.

    Args:
        service_account (string): Filepath to Google Service Account client secrets JSON keyfile
        request (protobuf): API query in Protocol Buffer or Protobuf format

    Returns:
        df (dataframe): Pandas dataframe of results.
    """

    response = _get_request(service_account, request)
    df = _to_dataframe(response)

    return df


def get_metadata(service_account, property_id):
    """Return metadata for the Google Analytics property.
    Args:
        service_account (string): Filepath to Google Service Account client secrets JSON keyfile
        property_id (string): Google Analytics 4 property ID

    Returns:
        df (dataframe): Pandas dataframe of metadata for the property.
    """

    client = _get_client(service_account)
    request = GetMetadataRequest(name=f"properties/{property_id}/metadata")
    response = client.get_metadata(request)

    metadata = []
    for dimension in response.dimensions:
        metadata.append({
            "Type": "Dimension",
            "Data type": "STRING",
            "API Name": dimension.api_name,
            "UI Name": dimension.ui_name,
            "Description": dimension.description,
            "Custom definition": dimension.custom_definition
        })

    for metric in response.metrics:
        metadata.append({
            "Type": "Metric",
            "Data type": MetricType(metric.type_).name,
            "API Name": metric.api_name,
            "UI Name": metric.ui_name,
            "Description": metric.description,
            "Custom definition": metric.custom_definition
        })

    return pd.DataFrame(metadata).sort_values(by=['Type', 'API Name']).drop_duplicates()

