
### -------- IMPORTS -----------------------------------------------------------------------------------------

import pandas as pd
from tqdm import tqdm
import datetime
from disaster_extr_constants import *


### ------------------ HELPER FUNCTIONS -----------------------------------------------------------------------

def df_time_interval(df, start, end, date_attr='StartDate'):
    time_mask = ((df[date_attr]>=start) & (df[date_attr]<=end))
    return df.loc[time_mask]

def extract_quotes(df, regex, field='quotation', complement=False):
    mask = df[field].str.contains(regex)
    if complement:
        mask = ~mask
    return df[mask]

def extract_quotes_protected(df, protected_regex, unwanted_regex, field='quotation', with_url=False):
    mask_protected = df[field].str.contains(protected_regex)
    df_protected_index = set(df[mask_protected].index)

    mask_unwanted = df[field].str.contains(unwanted_regex)
    df_unwanted_index = set(df[mask_unwanted].index)
    
    if with_url:
        url_regex, url_field = with_url[0], with_url[1]
        mask_protected_url = df[url_field].str.contains(url_regex)
        df_protected_url_index = set(df[mask_protected_url].index)
        df_protected_index.update(df_protected_url_index)
        
        if len(with_url) > 2:
            url_regex, url_field = with_url[2], with_url[3]
            mask_unwanted_url = df[url_field].str.contains(url_regex)
            df_unwanted_url_index = set(df[mask_unwanted_url].index)
            df_unwanted_index.update(df_unwanted_url_index)   
        
    
    resulting_inices = list(df_unwanted_index - df_protected_index)
    return df.drop(resulting_inices)

def get_df_disaster(df, year_to_id_map, set_val=None):
    IDS = sum(year_to_id_map.values(), [])
    mask = df.index.isin(IDS)
    df_disasters = df.loc[mask]
    if set_val:
        for key, value in set_val.items():
            for key_, value_ in value.items():
                df_disasters.at[key, key_] = value_
    return df_disasters

def retrieve_bounding_dates(df_disaster):
    grouped = df_disaster.groupby(df_disaster.StartDate.dt.year)
    aggregated = grouped.agg({'StartDate':'min', 'EndDate':'max'})
    aggregated.index.names = ['Year']
    aggregated.columns = ['MinStartDate', 'MaxEndDate']
    return aggregated

def compute_date_bounds(start, end):
    d = datetime.timedelta(days=21)
    lower = start - d
    duration = end - start 
    if duration.days > 30:
        upper = end
    else: 
        upper = end + d
    return lower.strftime("%Y-%m-%d"), upper.strftime("%Y-%m-%d")

def compute_n_rows(path_to_file, compression='bz2', chunksize=1000000):
    count = 0
    with pd.read_json(path_to_file,lines=True,compression=compression,chunksize=chunksize) as df_reader: 
        for chunk in tqdm(df_reader):
            count += len(chunk)
    return count

def write_df_to_disk(df, disaster_type, year, additional_text='climate_processed', compression='bz2', file_type='csv'):
    if file_type == 'csv':
        df.to_csv('data/'+str(year)+'_'+disaster_type+'_'+additional_text+'_csv.bz2',index=False, compression=compression)
    elif file_type == 'json':
        df.to_json('data/'+str(year)+'_'+disaster_type+'_'+additional_text+'_json.bz2', compression=compression)
    elif file_type == 'both':
        write_df_to_disk(df, disaster_type, year, compression=compression, file_type='csv')
        write_df_to_disk(df, disaster_type, year, compression=compression, file_type='json')
    else:
        print("Type must be csv or json (or both)!")   

def generate_regex_from_year_and_type(year, disaster_type, include_climate=True):
    
    # Dict mapping year to a second dict mapping disaster type to 
    # corresponding tag dict
    year_to_tags = {
        2015: {'storm': storm_tags_2015, 'heat_wave': heat_tags_2015},
        2016: {'storm': storm_tags_2016, 'heat_wave': heat_tags_2016},
        2017: {'storm': storm_tags_2017, 'heat_wave': heat_tags_2017},
        2018: {'storm': storm_tags_2018, 'heat_wave': heat_tags_2018},
        2019: {'storm': storm_tags_2019, 'heat_wave': heat_tags_2019}, 
        2020: {'storm': storm_tags_2020, 'heat_wave': heat_tags_2020}
    }
    
    # Dict mapping disaster type to corresponding tag dict
    type_to_tags = {
        'storm': storm_tags,
        'heat_wave': heat_tags
    }
    
    # List of all tags
    year_type_tag_list = year_to_tags[year][disaster_type].tags.values.tolist()
    type_tag_list = type_to_tags[disaster_type].tags.values.tolist()
    all_disaster_tags = year_type_tag_list + type_tag_list

    # Include climate tags or not (most often yes)
    if include_climate:
        all_disaster_tags.extend(climate_tags.tags.values.tolist())
        
    # Return regex pattern
    return r'|'.join(all_disaster_tags)

def process_quotes(data_path, lower_YEAR, upper_YEAR, year, regex_pattern, compression='bz2',chunksize=100000):
    chunk_interval_list = []
    with pd.read_json(data_path,lines=True,compression=compression,chunksize=chunksize) as df_reader:
        print('Reading chunks of size {} from {} dataset.'.format(chunksize, year))
        for chunk in tqdm(df_reader):
            chunk_interval = chunk[(chunk['date'] >= lower_YEAR) & (chunk['date'] <= upper_YEAR)]
            chunk_interval_list.append(chunk_interval[chunk_interval['quotation'].str.contains(regex_pattern)])
    return pd.concat(chunk_interval_list)

def process_quotes_both_disaster_and_climate(data_path, year, regex_pattern_disaster, regex_pattern_climate, compression='bz2',chunksize=100000, skip_climate=False):
    chunk_interval_list_disaster = []
    chunk_interval_list_climate = []
    with pd.read_json(data_path,lines=True,compression=compression,chunksize=chunksize) as df_reader:
        print('Reading chunks of size {} from {} dataset.'.format(chunksize, year))
        for chunk in tqdm(df_reader):
            chunk_interval_list_disaster.append(chunk[chunk['quotation'].str.contains(regex_pattern_disaster)])
            if not skip_climate:
                chunk_interval_list_climate.append(chunk[chunk['quotation'].str.contains(regex_pattern_climate)])

    if skip_climate:
        climate_return = None
    else: 
        climate_return = pd.concat(chunk_interval_list_climate)

    return pd.concat(chunk_interval_list_disaster), climate_return

def get_disaster_df_from_type(disaster_type, storm_df, heat_wave_df):
    if disaster_type == 'storm':
        return storm_df
    elif disaster_type == 'heat_wave':
        return heat_wave_df
    else:
        print("Error: disaster type must be either 'storm' or 'heat_wave'!")