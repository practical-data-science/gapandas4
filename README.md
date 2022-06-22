# GAPandas4
GAPandas4 is a Python package for querying the Google Analytics Data API for GA4 and displaying the results in a Pandas dataframe. It is the successor to the GAPandas package, which did the same thing for GA3 or Universal Analytics. GAPandas4 is a wrapper around the official Google Analytics Data API package and simplifies imports and queries, requiring far less code. 

### Before you start
In order to use GAPandas4 you will first need to create a Google Service Account with access to the Google Analytics Data API and export a client secrets JSON keyfile to use for authentication. You'll also need to add the service account email address as a user on the Google Analytics 4 property you wish to access, and you'll need to note the property ID to use in your queries. There's more information on that here. 

### Installation
As this is currently in alpha, there's currently no Pip package, however, you can install the code into your Python environment directly from GitHub using the command below. It will run fine in a Jupyter notebook, a Python IDE, or a Python script. 

### Usage
GAPandas4 has been written to allow you to use as little code as possible. Unlike the previous version of GAPandas for Universal Analytics, which used a payload based on a Python dictionary, GAPandas4 now uses a Protobuf (Protocol Buffer) payload as used in the API itself. 

Providing there's data in your Google Analytics 4 property, the below query should return a Pandas dataframe of your data. 

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

