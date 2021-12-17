"""
Extract quotes from Quotebank for --general-- heat waves and storms in each 
year between 2015 and 2020. Quotes about climate change are also collected
in order to evaluate the existence (or not) of a relationship between the 
frequencies of the two.
"""

### -------- IMPORTS -----------------------------------------------------------------------------------------

import pandas as pd
from disaster_extr_constants import *
from disaster_extr_helpers import *

compression = 'bz2'
chunksize = 100000

YEARS = [2015, 2016, 2017, 2018, 2019, 2020]
disaster_types = ['storm', 'heat_wave']

### ------------------ RUN -----------------------------------------------------------------------

for YEAR in YEARS:

    data_path = '../data/quotes-'+str(YEAR)+'.json.bz2'
    
    for disaster_type in disaster_types:

        if disaster_type == 'storm':
            disaster_tag_list = storm_tags_general.tags.values.tolist()
            skip_climate = False
        else:
            skip_climate = True
            disaster_tag_list = heat_tags_general.tags.values.tolist()

        regex_pattern_disaster = r'|'.join(disaster_tag_list)

        climate_tag_list = climate_tags_pos.tags.values.tolist()
        regex_pattern_climate = r'|'.join(climate_tag_list)

        all_data = process_quotes_both_disaster_and_climate(data_path, YEAR, regex_pattern_disaster, regex_pattern_climate, compression=compression,chunksize=100000, skip_climate=skip_climate)
        df_concat_result_disaster = all_data[0]
        write_df_to_disk(df_concat_result_disaster, disaster_type, YEAR, additional_text='whole_year', compression=compression, file_type='csv')

        print("Wrote {} {} quotes to disk.".format(YEAR, disaster_type))

        if not skip_climate:
            df_concat_result_climate = all_data[1]
            write_df_to_disk(df_concat_result_climate, 'climate', YEAR, additional_text='whole_year', compression=compression, file_type='csv')
            print("Wrote {} climate quotes to disk.".format(YEAR))
