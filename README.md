# GAPandas4
GAPandas4 is a Python package for querying the Google Analytics Data API for GA4 and displaying the results in a Pandas dataframe. It is the successor to the [GAPandas](https://practicaldatascience.co.uk/data-science/how-to-access-google-analytics-data-in-pandas-using-gapandas) package, which did the same thing for GA3 or Universal Analytics. GAPandas4 is a wrapper around the official Google Analytics Data API package and simplifies imports and queries, requiring far less code. 

### Before you start
In order to use GAPandas4 you will first need to [create a Google Service Account](https://practicaldatascience.co.uk/data-engineering/how-to-create-a-google-service-account-client-secrets-json-key) with access to the Google Analytics Data API and export a client secrets JSON keyfile to use for authentication. You'll also need to add the service account email address as a user on the Google Analytics 4 property you wish to access, and you'll need to note the property ID to use in your queries.  

### Installation
As this is currently in alpha, there's currently no Pip package, however, you can install the code into your Python environment directly from GitHub using the command below. It will run fine in a Jupyter notebook, a Python IDE, or a Python script. 

```commandline
pip3 install git+https://github.com/practical-data-science/gapandas4.git
```

### Usage
GAPandas4 has been written to allow you to use as little code as possible. Unlike the previous version of GAPandas for Universal Analytics, which used a payload based on a Python dictionary, GAPandas4 now uses a Protobuf (Protocol Buffer) payload as used in the API itself. Providing there's data in your Google Analytics 4 property, the below query should return a Pandas dataframe of your data. 

#### `run_report()`
The `run_report()` function is used for running regular reports and queries. It takes a `service_account` filepath and a Protobuf request. Further usage examples for `run_report()` can be found in this post: [How to query the Google Analytics Data API for GA4 using Python
](https://practicaldatascience.co.uk/data-science/how-to-query-the-google-analytics-data-api-for-ga4-with-python) 

```python
import gapandas4 as gp

service_account = 'client_secrets.json'
property_id = '123456789'

request = gp.RunReportRequest(
    property=f"properties/{property_id}",
    dimensions=[
        gp.Dimension(name="country"),
        gp.Dimension(name="city")
    ],
    metrics=[
        gp.Metric(name="activeUsers")
    ],
    date_ranges=[gp.DateRange(start_date="2022-06-01", end_date="2022-06-01")],
)

df = gp.run_report(service_account, request)
print(df.head())
```

#### `get_metadata()`
The `get_metadata()` function will return all metadata on dimensions and metrics within the Google Analytics 4 property. 

```python
metadata = gp.get_metadata(service_account, property_id)
print(metadata)
```

### Current features
- `DateRange`, `Dimension`, `Metric`, `OrderBy`, `Filter`, `FilterExpression`, and `FilterExpressionList` all work with `RunReportRequest` via `run_report()`. However, `MetricAggregation` is not implemented as it's so easy to calculate the total, maximum, and minimum of a column in Pandas itself.
- `get_metadata()` will return all metadata for the Google Analytics 4 property. 