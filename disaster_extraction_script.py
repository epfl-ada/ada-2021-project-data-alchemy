### -------- IMPORTS -----------------------------------------------------------------------------------------

import pandas as pd
from disaster_extr_constants import *
from disaster_extr_helpers import *

compression = 'bz2'
chunksize = 100000

YEARS = [2015, 2016, 2017, 2018, 2019] # Treat 2020 at the bottom
disaster_types = ['storm', 'heat_wave']

### ------------------ RUN -----------------------------------------------------------------------

data = 'data/emdat_processed.csv'
parse_dates = ['StartDate', 'EndDate']
df_emdat = pd.read_csv(data, index_col="Dis No", parse_dates = parse_dates)



df_heat_wave = get_df_disaster(df_emdat, HEAT_WAVES, HEAT_WAVES_val)
df_heat_wave_bounds = retrieve_bounding_dates(df_heat_wave)

df_storm = get_df_disaster(df_emdat, STORMS, STORMS_val)
df_storm_bounds = retrieve_bounding_dates(df_storm)

disaster_to_date_df = {'storm': df_storm_bounds, 'heat_wave': df_heat_wave_bounds}

for YEAR in YEARS:

    data_path = 'data/quotes-'+str(YEAR)+'.json.bz2'
    
    for disaster_type in disaster_types:
        
        disaster_df_bounds = disaster_to_date_df[disaster_type]

        start_YEAR, end_YEAR = disaster_df_bounds.loc[YEAR].MinStartDate, disaster_df_bounds.loc[YEAR].MaxEndDate
        lower_YEAR, upper_YEAR = compute_date_bounds(start_YEAR, end_YEAR)

        regex_pattern = generate_regex_from_year_and_type(YEAR, disaster_type)

        df_concat_result = process_quotes(data_path,lower_YEAR,upper_YEAR,YEAR,regex_pattern,compression=compression,chunksize=chunksize)

        write_df_to_disk(df_concat_result, disaster_type, YEAR, compression=compression, file_type='both')

# Treat special case of 2020 heat wave because quotes are split between 2019 and 2020

YEAR = 2020
disaster_type = "heat_wave"

df_heat_wave_2020 = get_df_disaster(df_emdat, HEAT_WAVES_2020, HEAT_WAVES_2020_val)
df_heat_wave_2020_bounds = retrieve_bounding_dates(df_heat_wave_2020)

start_2019, end_2020 = df_heat_wave_2020_bounds.loc[YEAR-1].MinStartDate, df_heat_wave_2020_bounds.loc[YEAR-1].MaxEndDate
lower_2019, upper_2020 = compute_date_bounds(start_2019, end_2020)

upper_2019 = datetime.datetime(2019, 12, 31).strftime("%Y-%m-%d")
lower_2020 = datetime.datetime(2020, 1, 1).strftime("%Y-%m-%d")

regex_pattern = generate_regex_from_year_and_type(YEAR, disaster_type)

data_path_2019 = 'data/quotes-'+str(YEAR-1)+'.json.bz2'
df_concat_result_2019 = process_quotes(data_path_2019,lower_2019,upper_2019,YEAR-1,regex_pattern,compression=compression,chunksize=chunksize)

data_path_2020 = 'data/quotes-'+str(YEAR)+'.json.bz2'
df_concat_result_2020 = process_quotes(data_path_2020,lower_2020,upper_2020,YEAR,regex_pattern,compression=compression,chunksize=chunksize)

df_list = [df_concat_result_2019, df_concat_result_2020]

df_concat_result = pd.concat(df_list)

len_row_match = len(df_concat_result_2019) + len(df_concat_result_2020) == len(df_concat_result)
print("Do row lengths match: {}".format(len_row_match))

len_col_match = len(df_concat_result_2019.columns) == len(df_concat_result_2020.columns) == len(df_concat_result.columns)
print("Do column lengths match: {}".format(len_col_match))

write_df_to_disk(df_concat_result, disaster_type, YEAR, compression=compression, file_type='both')

# Treat special case of 2020 storm because it is actually from 2019

YEAR = 2020
disaster_type = "storm"

df_storm_2020 = get_df_disaster(df_emdat, STORMS_2020, STORMS_2020_val)
df_storm_2020_bounds = retrieve_bounding_dates(df_storm_2020)

start_2019, end_2019 = df_storm_2020_bounds.loc[YEAR-1].MinStartDate, df_storm_2020_bounds.loc[YEAR-1].MaxEndDate
lower_2019, upper_2019 = compute_date_bounds(start_2019, end_2019)

regex_pattern = generate_regex_from_year_and_type(YEAR, disaster_type)

data_path_2019 = 'data/quotes-'+str(YEAR-1)+'.json.bz2'
df_concat_result_2019 = process_quotes(data_path_2019,lower_2019,upper_2019,YEAR-1,regex_pattern,compression=compression,chunksize=chunksize)

write_df_to_disk(df_concat_result_2019, disaster_type, YEAR, compression=compression, file_type='both')