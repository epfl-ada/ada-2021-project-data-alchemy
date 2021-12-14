# **Data**

## **Processed Data**

For each disaster type (storm or heat wave) there is a file ``YEAR_DISASTER_TYPE_filtered_csv.bz2`` which contains all quotes pertaining to the corresponding natural disaster during its timeframe (start and end dates from emdat dataset). If, however, the natural disaster lasted less than 31 days, the quotes are in the time interval [start, end + 10 days].