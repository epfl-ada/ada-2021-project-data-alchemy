# **Data**

## **Processed Data**

We extract tokens pertaining to heat waves, storms and the general token 'especially' for each year. These are stored as ``YEAR_DISASTER_TYPE_whole_year_csv.bz2`` and ``YEAR_especially__csv.bz2``

The other more specific disasters for each year were extracted but ultimately not used. So the below part can be ignored.

For each disaster type (storm or heat wave) there is a file ``YEAR_DISASTER_TYPE_filtered_csv.bz2`` which contains all quotes pertaining to the corresponding natural disaster during its timeframe (start and end dates from emdat dataset). If, however, the natural disaster lasted less than 31 days, the quotes are in the time interval [start, end + 10 days]. Additionally, certain storms (2016, 2017, 2018, 2019) have quotes from the interval [start - 2 days, end + 10 days] (start - 5 days for 2019) since storms can (and often do) appear in the news before they 'hit'.

### Heat Wave: 
- May 2015 India -> google trends indicates increase in climate change with disaster (avoid end of year because of Paris climate agreement being signed)
- April May 2016 India heat wave
- February 2017 Australia heat wave
- 2018 Japan/Korea July heat wave
- July 2019 Europe heat wave
- September 2019 - Jan 2020 Australia Bushfire/Heat Wave

### Storm/Cyclone/Hurricane:
- October 2015 Hurricane Patricia Mexico 
- February 2016 Cyclone Winston Fiji
- September 2017 Hurricane Harvey United States
- September 2018 Hurricane Florence in US + Typhoon Mangkhut (Ompong) in Philippines / China
- October 2019 Hagibis Typhoon Japan 
- December 2020 Tropical cyclone 'Kammuri' (Tisoy) in Philippines