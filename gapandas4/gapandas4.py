"""
GAPandas4
"""

import os
import pandas as pd
from google.analytics.data_v1beta import BetaAnalyticsDataClient


def _get_client(service_account):
    """Create a connection using a service account"""

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = service_account
    client = BetaAnalyticsDataClient()

    return client


def _get_request(service_account, request):
    """Pass a request to the API and return a response"""

    client = _get_client(service_account)
    response = client.run_report(request)
    return response


def _get_headers(response):
    """Return a Python list of dimension and metric header names from the Protobuf response.
    """

    headers = []

    for header in response.dimension_headers:
        headers.append(header.name)

    for header in response.metric_headers:
        headers.append(header.name)

    return headers


def _get_rows(response):
    """Return a Python list of row value lists from the Protobuf response.
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
    """Returns a Pandas dataframe of results."""

    headers = _get_headers(response)
    rows = _get_rows(response)
    df = pd.DataFrame(rows, columns=headers)

    return df


def run_report(service_account, request):
    """Pass a Protobuf request to the GA4 API using runReport and return a Pandas dataframe.
    """

    response = _get_request(service_account, request)
    df = _to_dataframe(response)

    return df

