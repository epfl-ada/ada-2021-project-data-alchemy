# **Data**

## **Processed Data**

For each disaster type (storm or heat wave) there is a file ``YEAR_DISASTER_TYPE_filtered_csv.bz2`` which contains all quotes pertaining to the corresponding natural disaster during its timeframe (start and end dates from emdat dataset). If, however, the natural disaster lasted less than 31 days, the quotes are in the time interval [start, end + 10 days]. Additionally, certain storms (2016, 2017, 2018, 2019) have quotes from the interval [start - 2 days, end + 10 days] (start - 5 days for 2019) since storms can (and often do) appear in the news before they 'hit'.