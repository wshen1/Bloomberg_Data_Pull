# MMF 1941: The Bloomberg Data Download Guide

This guide covers the two primary methods for systematically downloading data from Bloomberg for your project: the **Python API (`blpapi`)** and the **Excel Add-in**.

**Key Recommendation:** For any large-scale, systematic data collection for your team's charter, the **Python API is the strongly preferred method**. It is more efficient, scalable, and reproducible. The Excel Add-in is best for quick, exploratory analysis and for discovering the correct field mnemonics.

---

## Method 1: The Python API (`blpapi`)

The Bloomberg API allows you to programmatically request data directly within a Python script or Jupyter Notebook.

### A. First-Time Setup
You only need to do this once on any machine you use.
1.  **Install the library:** Open a terminal or command prompt and run:
    ```sh
    pip install blpapi
    ```
2.  **Ensure Bloomberg is Running:** The Bloomberg Terminal software must be running and you must be logged in for the API to connect.

### B. Example: Downloading Historical Data
This is the most common task you will perform. The following code downloads the daily closing price and trading volume for Apple and Microsoft for the year 2024.

```python
# Import the necessary libraries
import blpapi
import pandas as pd

# Define constants for the API session
SESSION_STARTED = blpapi.Name("SessionStarted")
SESSION_STARTUP_FAILURE = blpapi.Name("SessionStartupFailure")
SERVICE_OPENED = blpapi.Name("ServiceOpened")
SERVICE_OPEN_FAILURE = blpapi.Name("ServiceOpenFailure")
ERROR_INFO = blpapi.Name("ErrorInfo")
SECURITY_DATA = blpapi.Name("securityData")

# --- Main Function to Get Bulk Historical Data ---
def get_bdh_data(tickers, fields, start_date, end_date):
    """
    Downloads historical data (BDH) from the Bloomberg API.
    """
    # Boilerplate connection logic
    sessionOptions = blpapi.SessionOptions()
    sessionOptions.setServerHost('localhost')
    sessionOptions.setServerPort(8194)
    session = blpapi.Session(sessionOptions)

    if not session.start():
        print("Failed to start session.")
        return

    if not session.openService("//blp/refdata"):
        print("Failed to open //blp/refdata")
        return

    refDataService = session.getService("//blp/refdata")
    request = refDataService.createRequest("HistoricalDataRequest")

    # Add tickers and fields to the request
    for ticker in tickers:
        request.getElement("securities").appendValue(ticker)
    for field in fields:
        request.getElement("fields").appendValue(field)

    # Set request parameters
    request.set("periodicitySelection", "DAILY")
    request.set("startDate", start_date)
    request.set("endDate", end_date)

    session.sendRequest(request)
    
    all_data = []
    
    # Process the response events
    while(True):
        ev = session.nextEvent(500)
        for msg in ev:
            if msg.hasElement(SECURITY_DATA):
                sec_data = msg.getElement(SECURITY_DATA)
                ticker = sec_data.getElementAsString("security")
                field_data = sec_data.getElement("fieldData")
                for i in range(field_data.numValues()):
                    row = field_data.getValueAsElement(i)
                    date = row.getElementAsDatetime("date").date()
                    for field in fields:
                        if row.hasElement(field):
                            value = row.getElementAsFloat(field)
                            all_data.append([date, ticker, field, value])
        if ev.eventType() == blpapi.Event.RESPONSE:
            break
            
    session.stop()
    
    # Convert the received data to a pandas DataFrame
    df = pd.DataFrame(all_data, columns=['date', 'ticker', 'field', 'value'])
    # Pivot the table to a more usable format
    pivot_df = df.pivot_table(index='date', columns=['ticker', 'field'], values='value')
    return pivot_df

# --- Example Usage ---
if __name__ == '__main__':
    tickers_to_load = ["AAPL US Equity", "MSFT US Equity"]
    fields_to_load = ["PX_LAST", "PX_VOLUME"]
    start = "20240101"
    end = "20241231"
    
    historical_data = get_bdh_data(tickers_to_load, fields_to_load, start, end)
    
    if historical_data is not None:
        print("Successfully downloaded data:")
        print(historical_data.head())
````

-----

## Method 2: The Excel Add-in

The Bloomberg Excel Add-in is excellent for quickly pulling data, exploring what fields are available, and performing one-off analyses.

### A. Key Formulas

The two main formulas are `=BDP()` for a single data point and `=BDH()` for historical data.

  - **BDP (Bloomberg Data Point):** `=BDP("Security Ticker", "Field Mnemonic")`

      - Example: `=BDP("AAPL US Equity", "PX_LAST")` will return the current price of Apple stock.

  - **BDH (Bloomberg Data History):** `=BDH("Security Ticker", "Field Mnemonic", "Start Date", "End Date")`

      - Example: `=BDH("SPX Index", "PX_LAST", "2024-01-01", "2024-12-31")` will return the daily closing price of the S\&P 500 for 2024.

### B. Using the Formula Builder (Recommended)

Manually typing these formulas can be error-prone. The best way to use the Add-in is with the **Spreadsheet Builder**.

1.  In Excel, go to the **Bloomberg** tab.
2.  Click on **Spreadsheet Builder**.
3.  A sidebar will open. Select **Historical Data Table** and click Next.
4.  You can now search for your securities, search for your fields, and select a date range using a graphical interface.
5.  This will build the formula for you and place the data directly into your sheet.

### C. Comparison of Methods

| Feature | Python API (`blpapi`) | Excel Add-in |
| :--- | :--- | :--- |
| **Best For** | Large, systematic data collection. | Quick lookups, field discovery. |
| **Scalability** | **Excellent.** Can download data for thousands of tickers automatically. | **Poor.** Mostly manual process. |
| **Reproducibility** | **Excellent.** The code is a perfect record of how the data was obtained. | **Poor.** It's hard to document the exact steps taken. |
| **Learning Curve** | Moderate. Requires basic Python knowledge. | Low. Very easy to get started. |