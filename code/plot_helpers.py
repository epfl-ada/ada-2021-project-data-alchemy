"""
Functions for generating plots of the extracted quote data.
"""

### -------- IMPORTS -----------------------------------------------------------------------------------------

import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from disaster_extr_helpers import extract_disaster

### ------------------ HELPER FUNCTIONS -----------------------------------------------------------------------

def compute_relevant_spikes(specific_data, 
                            general_data, 
                            specific_general_increase=2.5,
                            specific_increase=0.1):
    """
    Function to compute relevant spikes in quote data.
    """
    # Compute time shifted versions of both input arrays
    shifted_specific = np.concatenate(([specific_data[0]],specific_data[:-1]))
    shifted_general = np.concatenate(([general_data[0]],general_data[:-1]))
    
    # Compute respective differences (to capture increases)
    specific_difference = specific_data - shifted_specific
    general_difference = general_data - shifted_general
    
    # Compute difference between increases in specific quotes (climate or disaster)
    # general quote (contains 'especially'). Possibility to use a factor
    # to raise the factor by white the specific increase must surpass the general increase
    increase_by_factor = specific_difference - general_difference * specific_general_increase
    
    # When (i.e., for a given time index) specific increase is 'specific_general_increase' 
    # times higher than the general increase and the specific increase is greater 
    # than 'specific_increase' return the corresponding entry from 'specific_data',
    # otherwise return 0
    
    out = np.where(((increase_by_factor > 0) & (specific_difference >= specific_increase)), 
                   specific_data, 0)
    return out

def create_plot_comparison(year,
                           disaster_type,
                           general=False,
                           resample=None, 
                           normalize=False, 
                           log=True, 
                           norm_additional=False,
                           drop_n_first=0,
                           drop_n_last=0,
                           save_fig=False):
        
    all_data = extract_disaster(year,disaster_type,general)
    
    (climate_df, start_climate, end_climate) = all_data[0]
    (disaster_df, start_disaster, end_disaster) = all_data[1]
    disaster_df_2 = all_data[2]
    
    if resample:
        climate_df.at[0, 'date'] = datetime.datetime(year, 1, 1)
        disaster_df.at[0, 'date'] = datetime.datetime(year, 1, 1)
        climate_df = climate_df.set_index('date').resample(resample).sum().dropna().reset_index()
        disaster_df = disaster_df.set_index('date').resample(resample).sum().dropna().reset_index()
        
        climate_df.drop(climate_df.tail(drop_n_last).index,inplace=True)
        climate_df.drop(climate_df.head(drop_n_first).index,inplace=True)
        disaster_df.drop(disaster_df.tail(drop_n_last).index,inplace=True)
        disaster_df.drop(disaster_df.head(drop_n_first).index,inplace=True)
            
        if normalize:
            x_climate = climate_df.numOccurrences.values.reshape(-1, 1)
            min_max_scaler_climate = preprocessing.MinMaxScaler().fit(x_climate)
            x_climate_scaled = min_max_scaler_climate.transform(x_climate)
            
            x_disaster = disaster_df.numOccurrences.values.reshape(-1, 1)
            min_max_scaler_disaster = preprocessing.MinMaxScaler().fit(x_disaster)
            x_disaster_scaled = min_max_scaler_disaster.transform(x_disaster)
            
            climate_df.numOccurrences = pd.DataFrame(x_climate_scaled)
            disaster_df.numOccurrences = pd.DataFrame(x_disaster_scaled)
            
        if norm_additional:
            norm_path = '../data/'+str(year)+'_especially__csv.bz2'
            norm_df = pd.read_csv(norm_path, parse_dates = ['date'], compression='bz2')
            norm_df.at[0, 'date'] = datetime.datetime(year, 1, 1)

            norm_df = norm_df.set_index('date').resample(resample).sum().dropna().reset_index()
            
            norm_df.drop(norm_df.tail(drop_n_last).index,inplace=True)
            norm_df.drop(norm_df.head(drop_n_first).index,inplace=True)
            
            # Unnaturally big spike in 2018, remove it (set to mean) to keep meaningful variance
            if year == 2018:
                norm_df.at[norm_df.idxmax().numOccurrences, 'numOccurrences'] = norm_df.numOccurrences.mean()
            
            if normalize:
                x_norm = norm_df.numOccurrences.values.reshape(-1, 1)
                min_max_scaler = preprocessing.MinMaxScaler()
                x_norm_scaled = min_max_scaler.fit_transform(x_norm)
                norm_df.numOccurrences = pd.DataFrame(x_norm_scaled)
                
                
    if disaster_df_2 is not None:
        dscr_str = 'Asia'
        dscr_str_2 = 'America'
        if resample:
            disaster_df_2 = disaster_df_2.set_index('date').resample(resample).sum().dropna().reset_index()
            
            if normalize:
                x_disaster_2 = disaster_df_2.numOccurrences.values.reshape(-1, 1)
                min_max_scaler = preprocessing.MinMaxScaler()
                x_disaster_2_scaled = min_max_scaler.fit_transform(x_disaster_2)                
                disaster_df_2.numOccurrences = pd.DataFrame(x_disaster_2_scaled)
                    
    else:
        dscr_str = ''
    
    print("Disaster Dates: {} --- {}".format(
            start_disaster.strftime("%Y-%m-%d"), 
            end_disaster.strftime("%Y-%m-%d")))
    print("Climate Dates:  {} --- {}".format(
            start_climate.strftime("%Y-%m-%d"), 
            end_climate.strftime("%Y-%m-%d")))
    
    type_to_str = {
        'storm': str(year) + ' Storm ',
        'heat_wave': str(year) + ' Heat Wave ',
    } 
    
    
    type_to_str = {
        'storm': 'Storm ',
        'heat_wave': 'Heat Wave ',
    }
    
    fig = plt.gcf()
    fig.set_size_inches(14, 5)
    plt.grid()
    
    plt.plot(
    climate_df.date,  
    climate_df.numOccurrences,
    alpha=0.4,
    label='Climate Data',
    marker='o')
    
    plt.plot(
    disaster_df.date,  
    disaster_df.numOccurrences,
    alpha=0.7,
    label=type_to_str[disaster_type]+dscr_str+' Data',
    marker='o')
    
    
    if norm_additional:
        plt.plot(
        norm_df.date,  
        norm_df.numOccurrences,
        alpha=0.3,
        label='General Data',
        marker='o')
        
    if disaster_df_2 is not None:
        plt.plot(
        disaster_df_2.date,  
        disaster_df_2.numOccurrences,
        alpha=0.3,
        label=type_to_str[disaster_type]+dscr_str_2+' Talk',
        marker='o')
        
    if log:   
        plt.yscale('log')
    plt.xlabel("Time")
    plt.ylabel("Absolute Nº of Quotes (numOccurrences)")
    plt.title("Evolution of quote data throughout "+str(year)+".")
    plt.legend(loc='lower right')
    if save_fig:
        plt.savefig('images/'+str(year)+'_'+disaster_type+'.png', bbox_inches='tight')
    plt.show()

def create_normalized_comparison(year,
                                 disaster_type,
                                 resample='1W',
                                 drop_n_first=0,
                                 drop_n_last=0,
                                 specific_general_increase=2.5,
                                 specific_increase=0.1, 
                                 save_fig=False):
        
    all_data = extract_disaster(year,disaster_type,general=True)
    
    (climate_df, start_climate, end_climate) = all_data[0]
    (disaster_df, start_disaster, end_disaster) = all_data[1]
    disaster_df_2 = all_data[2]
    
    climate_df.at[0, 'date'] = datetime.datetime(year, 1, 1)
    disaster_df.at[0, 'date'] = datetime.datetime(year, 1, 1)
    climate_df = climate_df.set_index('date').resample(resample).sum().dropna().reset_index()
    disaster_df = disaster_df.set_index('date').resample(resample).sum().dropna().reset_index()
    
    climate_df.drop(climate_df.tail(drop_n_last).index,inplace=True)
    climate_df.drop(climate_df.head(drop_n_first).index,inplace=True)
    disaster_df.drop(disaster_df.tail(drop_n_last).index,inplace=True)
    disaster_df.drop(disaster_df.head(drop_n_first).index,inplace=True)

    x_climate = climate_df.numOccurrences.values.reshape(-1, 1)
    min_max_scaler = preprocessing.MinMaxScaler()
    x_climate_scaled = min_max_scaler.fit_transform(x_climate)

    x_disaster = disaster_df.numOccurrences.values.reshape(-1, 1)
    min_max_scaler = preprocessing.MinMaxScaler()
    x_disaster_scaled = min_max_scaler.fit_transform(x_disaster)
    
    climate_df.numOccurrences = pd.DataFrame(x_climate_scaled, index=climate_df.index)
    disaster_df.numOccurrences = pd.DataFrame(x_disaster_scaled, index=disaster_df.index)

    norm_path = '../data/'+str(year)+'_especially__csv.bz2'
    norm_df = pd.read_csv(norm_path, parse_dates = ['date'], compression='bz2')
    norm_df.at[0, 'date'] = datetime.datetime(year, 1, 1)

    norm_df = norm_df.set_index('date').resample(resample).sum().dropna().reset_index()
    
    norm_df.drop(norm_df.tail(drop_n_last).index,inplace=True)
    norm_df.drop(norm_df.head(drop_n_first).index,inplace=True)
    
    # Unnaturally big spike in 2018, remove it (set to mean) to keep meaningful variance
    if year == 2018:
        norm_df.at[norm_df.idxmax().numOccurrences, 'numOccurrences'] = norm_df.numOccurrences.mean()

    x_norm = norm_df.numOccurrences.values.reshape(-1, 1)
    min_max_scaler = preprocessing.MinMaxScaler()
    x_norm_scaled = min_max_scaler.fit_transform(x_norm)
    norm_df.numOccurrences = pd.DataFrame(x_norm_scaled, index=norm_df.index)

    climate_relevant_spikes = compute_relevant_spikes(x_climate_scaled.ravel(), 
                                                      x_norm_scaled.ravel(),
                                                      specific_general_increase,
                                                      specific_increase)
    disaster_relevant_spikes = compute_relevant_spikes(x_disaster_scaled.ravel(),
                                                       x_norm_scaled.ravel(),
                                                       specific_general_increase,
                                                       specific_increase)
    
    climate_df["spikes"] = pd.DataFrame(climate_relevant_spikes, index=climate_df.index)
    disaster_df["spikes"]  = pd.DataFrame(disaster_relevant_spikes, index=disaster_df.index)   
    
    if disaster_df_2 is not None:
        dscr_str = 'Asia'
        dscr_str_2 = 'America'
        if resample:
            disaster_df_2 = disaster_df_2.set_index('date').resample(resample).sum().dropna().reset_index()

            x_disaster_2 = disaster_df_2.numOccurrences.values.reshape(-1, 1)
            min_max_scaler = preprocessing.MinMaxScaler()
            x_disaster_2_scaled = min_max_scaler.fit_transform(x_disaster_2)

            x_disaster_2_scaled = compute_relevant_spikes(x_disaster_2_scaled.ravel(), x_norm_scaled.ravel())
            disaster_df_2.numOccurrences = pd.DataFrame(x_disaster_2_scaled)
                
                    
    else:
        dscr_str = ''
    
    print("Disaster Dates: {} --- {}".format(
            start_disaster.strftime("%Y-%m-%d"), 
            end_disaster.strftime("%Y-%m-%d")))
    print("Climate Dates:  {} --- {}".format(
            start_climate.strftime("%Y-%m-%d"), 
            end_climate.strftime("%Y-%m-%d")))
    
    type_to_str = {
        'storm': str(year) + ' Storm ',
        'heat_wave': str(year) + ' Heat Wave ',
    } 
    
    type_to_str = {
        'storm': 'Storm ',
        'heat_wave': 'Heat Wave ',
    } 
    
    fig = plt.gcf()
    fig.set_size_inches(14, 5)
    plt.grid()

    p = plt.plot(climate_df.date,  
                 climate_df.numOccurrences,
                 alpha=0.7,
                 label='Climate Data',
                 linestyle='--')
    
    climate_df = climate_df[climate_df.spikes > 0]
    
    plt.scatter(climate_df.date,  
                climate_df.spikes,
                alpha=1.0,
                color=p[0].get_color(),
                marker='o')

    p = plt.plot(disaster_df.date,  
                 disaster_df.numOccurrences,
                 alpha=0.7,
                 label=type_to_str[disaster_type]+dscr_str+' Data',
                 linestyle='--')
    
    disaster_df = disaster_df[disaster_df.spikes > 0]
    
    plt.scatter(disaster_df.date,  
                disaster_df.spikes,
                alpha=1.0,
                color=p[0].get_color(),
                marker='o')
    
    plt.plot(norm_df.date,  
             norm_df.numOccurrences,
             alpha=0.5,
             label='General Data',
             linestyle='--'
            )
    
    if disaster_df_2 is not None:
        plt.plot(
        disaster_df_2.date,  
        disaster_df_2.numOccurrences,
        alpha=0.3,
        label=type_to_str[disaster_type]+dscr_str_2+' Talk',
        marker='o')
        
    plt.xlabel("Time")
    plt.ylabel("Normalized Nº of Quotes (numOccurrences)")
    plt.title("Normalized evolution of quote data throughout "+str(year)+" with extracted relevant spikes.")
    plt.legend(loc='lower right')
    if save_fig:
        plt.savefig('images/'+str(year)+'_'+disaster_type+'_peaks.png', bbox_inches='tight')
    plt.show()


# Ultimately not used
def create_hist_comparison(year,disaster_type,general=False):
        
    all_data = extract_disaster(year,disaster_type,general)
    
    (climate_df, start_climate, end_climate) = all_data[0]
    (disaster_df, start_disaster, end_disaster) = all_data[1]
    disaster_df_2 = all_data[2]
    
    if disaster_df_2:
        dscr_str = 'Asia'
        dscr_str_2 = 'America'
    else:
        dscr_str = ''
    
    print("Disaster Dates: {} --- {}".format(
            start_disaster.strftime("%Y-%m-%d"), 
            end_disaster.strftime("%Y-%m-%d")))
    print("Climate Dates:  {} --- {}".format(
            start_climate.strftime("%Y-%m-%d"), 
            end_climate.strftime("%Y-%m-%d")))
    
    type_to_str = {
        'storm': str(year) + ' Storm ',
        'heat_wave': str(year) + ' Heat Wave ',
    } 
    
    fig = plt.gcf()
    fig.set_size_inches(14, 5)
    
    _, bins, _ = plt.hist(
        climate_df.date, 
        bins=60, 
        weights=climate_df.numOccurrences,
        alpha=0.4,
        label='Climate Talk', 
        log=True)
    
    plt.hist(
        disaster_df.date, 
        bins=bins, 
        weights=disaster_df.numOccurrences,
        alpha=0.7,
        label=type_to_str[disaster_type]+dscr_str+' Talk')
    
    if disaster_df_2:
        plt.hist(
            disaster_df_2.date, 
            bins=bins, 
            weights=disaster_df_2.numOccurrences,
            alpha=0.3,
            label=type_to_str[disaster_type]+dscr_str_2+' Talk')
    
    plt.xlabel("Time")
    plt.ylabel("Absolute Nº of Quotes (numOccurrences)")
    plt.title("Evolution of frequency of discussion around climate change and the specific disaster.")
    plt.legend(loc='upper left')
    plt.show()