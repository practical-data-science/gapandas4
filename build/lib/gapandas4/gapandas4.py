"""
GAPandas4
"""

import os
import pandas as pd
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import MetricType
from google.analytics.data_v1beta.types import GetMetadataRequest
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import OrderBy
from google.analytics.data_v1beta.types import Filter
from google.analytics.data_v1beta.types import Pivot
from google.analytics.data_v1beta.types import FilterExpression
from google.analytics.data_v1beta.types import FilterExpressionList
from google.analytics.data_v1beta.types import RunReportRequest
from google.analytics.data_v1beta.types import BatchRunReportsRequest
from google.analytics.data_v1beta.types import RunPivotReportRequest
from google.analytics.data_v1beta.types import BatchRunPivotReportsRequest
from google.analytics.data_v1beta.types import RunRealtimeReportRequest


def _get_client(service_account):
    """Create a connection using a service account.

    Args:
        service_account (string): Filepath to Google Service Account client secrets JSON keyfile

    Returns:
        client (object): Google Analytics Data API client
    """

    try:
        open(service_account)
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = service_account
        client = BetaAnalyticsDataClient()
        return client
    except Exception:
        print('Error: Google Service Account client secrets JSON key file does not exist')
        exit()


def _get_request(service_account, request, report_type="report"):
    """Pass a request to the API and return a response.

    Args:
        service_account (string): Filepath to Google Service Account client secrets JSON keyfile
        request (protobuf): API request in Protocol Buffer format.
        report_type (string): Report type (report, batch_report, pivot, batch_pivot, or realtime)

    Returns:
        response: API response.
    """

    client = _get_client(service_account)

    if report_type == "realtime":
        response = client.run_realtime_report(request)

    elif report_type == "pivot":
        response = client.run_pivot_report(request)

    elif report_type == "batch_pivot":
        response = client.batch_run_pivot_reports(request)

    elif report_type == "batch_report":
        response = client.batch_run_reports(request)

    else:
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


def _batch_to_dataframe_list(response):
    """Return a list of dataframes of results from a batchRunReports query.

    Args:
        response (object): Response object from a batchRunReports query.

    Returns:
        output (list): List of Pandas dataframes of results.
    """

    output = []
    for report in response.reports:
        output.append(_to_dataframe(report))
    return output


def _batch_pivot_to_dataframe_list(response):
    """Return a list of dataframes of results from a batchRunPivotReports query.

    Args:
        response (object): Response object from a batchRunPivotReports query.

    Returns:
        output (list): List of Pandas dataframes of results.
    """

    output = []
    for report in response.pivot_reports:
        output.append(_to_dataframe(report))
    return output


def _handle_response(response):
    """Use the kind to determine the type of report requested and reformat the output to a Pandas dataframe.

    Args:
        response (object): Protobuf response object from the Google Analytics Data API.

    Returns:
        output (dataframe, or list of dataframes): Return a single dataframe for runReport, runPivotReport,
        or runRealtimeReport
        or a list of dataframes for batchRunReports and batchRunPivotReports.
    """

    if response.kind == "analyticsData#runReport":
        return _to_dataframe(response)
    if response.kind == "analyticsData#batchRunReports":
        return _batch_to_dataframe_list(response)
    if response.kind == "analyticsData#runPivotReport":
        return _to_dataframe(response)
    if response.kind == "analyticsData#batchRunPivotReports":
        return _batch_pivot_to_dataframe_list(response)
    if response.kind == "analyticsData#runRealtimeReport":
        return _to_dataframe(response)
    else:
        print('Unsupported')


def query(service_account, request, report_type="report"):
    """Return Pandas formatted data for a Google Analytics Data API query.

    Args:
        service_account (string): Path to Google Service Account client secrets JSON key file
        request (protobuf): Google Analytics Data API protocol buffer request
        report_type (string): Report type (report, batch_report, pivot, batch_pivot, or realtime)

    Returns:
        output (dataframe, or list of dataframes): Return a single dataframe for runReport, runPivotReport,
        or runRealtimeReport
        or a list of dataframes for batchRunReports and batchRunPivotReports.
    """

    response = _get_request(service_account, request, report_type)
    output = _handle_response(response)
    return output


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

