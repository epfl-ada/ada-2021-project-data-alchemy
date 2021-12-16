"""
Extract quotes from Quotebank for the generic token 'especially' to get
statistics about overall quote frequency over a given year which is useful
to try and eliminate the influence of the variation of number of quotes over
a year when assessing the correlation between climate change and a natural disaster.
"""

### -------- IMPORTS -----------------------------------------------------------------------------------------

import pandas as pd
from disaster_extr_constants import *
from disaster_extr_helpers import *

compression = 'bz2'
chunksize = 100000

YEARS = [2015, 2016, 2017, 2018, 2019, 2020]
disaster_types = ['especially']

### ------------------ RUN -----------------------------------------------------------------------

for YEAR in YEARS:

    data_path = 'data/quotes-'+str(YEAR)+'.json.bz2'
    skip_climate = True

    regex_pattern_disaster = r'\b(especially)\b'
    disaster_type='especially'

    regex_pattern_climate = 'empty'

    all_data = process_quotes_both_disaster_and_climate(data_path, YEAR, regex_pattern_disaster, regex_pattern_climate, compression=compression,chunksize=100000, skip_climate=skip_climate)
    df_concat_result_disaster = all_data[0]
    write_df_to_disk(df_concat_result_disaster, disaster_type, YEAR, additional_text='', compression=compression, file_type='csv')

    print("Wrote {} {} quotes to disk.".format(YEAR, disaster_type))

