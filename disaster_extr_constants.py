### -------- IMPORTS -----------------------------------------------------------------------------------------

import pandas as pd

### ------------------ CONSTANTS-----------------------------------------------------------------------

australia_heat_wave = { 
    'Group': 'Natural',
    'Subgroup':'Meteorological', 
    'Type':'Extreme temperature ', 
    'Subtype':'Heat wave', 
    'Subsubtype': 'NaN',
    'Name':'NaN', 
    'Country':'Australia', 
    'ISO':'AUS', 
    'Region': 'Australia and New Zealand',
    'Continent': 'Oceania',
    'Origin':'NaN', 
    'Magnitude':48.2, 
    'Scale':'°C', 
    'Deaths': 0,
    'Injured':0, 
    'Affected':0,
    'Homeless':0,
    'TotalAffected':0, 
    'Damages':0, 
    'StartDate':'2017-01-30', 
    'EndDate': '2017-02-14',
    'Duration':15
}
# Not necessary, row already added to csv file
#row_series = pd.Series(data=australia_heat_wave, name='2017-9999-AUS')
#df_emdat = df_emdat.append(row_series, ignore_index=False)

STORMS = {
    '2015': ['2015-0470-MEX'],
    '2016': ['2016-0041-FJI'],
    '2017': ['2017-0362-USA'],
    '2018': ['2018-0342-USA', '2018-0341-CHN', '2018-0341-PHL', '2018-0341-HKG'], # two separate storms over same time period
    '2019': ['2019-0492-JPN'],
    #'2020': ['2020-0211-LKA', '2020-0211-BGD', '2020-0211-IND'] # can't use because in May 2020
}
STORMS_val = {
    '2018-0341-CHN': {'Magnitude': 240},
    '2018-0342-USA': {'Magnitude': 240, 'Damages': 24000000},
    #'2020-0211-BGD': {'Magnitude': 151},
    #'2020-0211-LKA': {'Magnitude': 80},
    '2018-0341-PHL': {'Deaths': 127, 'Damages': 628000},
    '2018-0341-CHN': {'Deaths': 6, 'Damages': 1990000},
    '2018-0341-HKG': {'Damages': 930000},
    '2017-0362-USA': {'Deaths': 106, 'Damages': 125000000},
    '2016-0041-FJI': {'Damages': 1400000},
    '2015-0470-MEX': {'Magnitude': 345, 'Damages': 462000}
}

STORMS_2020 = {
    '2020': ['2019-0573-PHL']
}
STORMS_2020_val = {}

HEAT_WAVES = {
    '2015': ['2015-0189-IND'],
    '2016': ['2016-0133-IND'],
    '2017': ['2017-9999-AUS', '2017-0072-AUS'], # heat wave and associated fire
    '2018': ['2018-0226-JPN', '2018-0256-PRK'],
    '2019': ['2019-0366-BEL', '2019-0366-FRA', '2019-0366-NLD', '2019-0366-DEU'], #'2019-0366-AUT' (no value for temp), '2019-0650-GBR' (lasts too long)
  #  '2020': ['2019-0545-AUS'] # Forest fire (can't use '2020-0441-USA' because in august)
}
HEAT_WAVES_val = {
    #'2020-0441-USA': {'Magnitude': 4180},
    '2017-0072-AUS': {'Magnitude': 550},
    '2018-0256-PRK': {'Deaths': 42},
    #'2019-0545-AUS': {'Magnitude': 186360}
}

HEAT_WAVES_2020 = {
    '2020': ['2019-0545-AUS'] # Forest fire (can't use '2020-0441-USA' because in august)
}
HEAT_WAVES_2020_val = {
    #'2020-0441-USA': {'Magnitude': 4180},
    '2019-0545-AUS': {'Magnitude': 186360}
}


# General tags for heat waves
heat_tags = pd.DataFrame(
    {'tags': [
        r'\b([dD]egrees)\b',
        r'\b([fF]ahrenheit)\b',
        r'\b(°[fF])\b',
        r'\b(°[cC])\b',
        r'\b([cC]elsius)\b',
        r'\b([mM]ercury (rose|hit))\b',
        #r'\b(waves?)\b', too broad
        r'\b([hH]eat(ing)?)\b',
        r'\b([tT]emperatures?)\b',
        r'\b([hH]ot(test|ter)?)\b',
        r'\b([wW]arm(er|est)?)\b',
        r'\b(([eE]xtreme|[vV]olatile) [wW]eather)\b',
        r'\b([hH]eatstrokes?)\b',
        r'\b([hH]eatwaves?)\b',
        r'\b([hH]eatstorms?)\b',
        r'\b([wW]orld [mM]eteorological [oO]rganisation)\b',
        r'\b(WMO)\b']
    }
)

# Indian Heat Wave 2015
heat_tags_2015 = pd.DataFrame(
    {'tags': [
        r'\b([aA]ndhra [pP]radesh)\b',
        r'\b([tT]elangana)\b',
        r'\b([pP]unjab)\b',
        r'\b([oO]disha)\b',
        r'\b([kK]hammam)\b',
        r'\b([jJ]harsuguda)\b',
        r'\b([hH]yderabad)\b',
        r'\b([iI]ndia [mM]eteorological [dD]epartment)\b']
    }
)

# Indian Heat Wave 2016
heat_tags_2016 = pd.DataFrame(
    {'tags': [
        r'\b([pP]halodi)\b',
        r'\b([iI]ndia [mM]eteorological [dD]epartment)\b']
    }
)

# Sir Ivan Fire (caused by heatwave) in Australia
heat_tags_2017 = pd.DataFrame(
    {'tags': [
        r'\b([bB]ureau [oF]f [mM]eteorology)\b',
        r'\b(New South Wales)\b',
        r'\b(Pilliga)\b',
        r'\b(Talleganda)\b',
        r'\b(Queensland Ambulance Service)\b',
        r'\b([wW]ildfires?)\b',
        r'\b([oO]range sk(y|ies))\b',
        r'\b([sS]moke clouds?)\b',
        r'\b(([bB]ush)?[fF]ires?)\b',
        r'\b([mM]egafires?)\b',
        r'\b([bB]urning forests?)\b',
        r'\b(Taree)\b',
        r'\b(Ivanhoe)\b']
    }
)

# Japan and Korea Heat Wave
heat_tags_2018 = pd.DataFrame(
    {'tags': [
        r'\b([kK]umagaya)\b',
        r'\b([jJ]apan [mM]eteorological [aA]gency)\b',
        r'\b([sS]henyang)\b',
        r'\b([tT]okyo [fF]ire [dD]epartment)\b',
        r'\b([gG]angneung)\b',
        r'\b([hH]ayang)\b']
    }
)

# Europe Heat Wave
heat_tags_2019 = pd.DataFrame(
    {'tags': [
        r'\b([aA]ngleur)\b',
        r'\b([bB]egijnendijk)\b',
        r'\b([dD]oksany)\b',
        r'\b([pP]orvoo)\b',
        r'\b([mM][ée]t[ée]o [fF]rance)\b',
        r'\b([gG]allargues-le-[mM]ontueux)\b',
        r'\b([bB]erlin[- ][tT]empelhof)\b',
        r'\b([bB]randenburg)\b',
        r'\b(Lingen)\b',
        r'\b([mM]eteolux)\b',
        r'\b([sS]teinsel)\b',
        r'\b(KNMI|knmi|[rR]oyal [dD]utch [mM]eteorological [iI]nstitute)\b',
        r'\b([gG]elderland)\b',
        r'\b([sS]altdal)\b',
        r'\b([nN]orwegian [mM]eteorological [iI]nstitute)\b',
        r'\b([zZ]aragoza)\b',
        r'\b([oO]skarshamn)\b',
        r'\b([sS]wedish [mM]eteorological and [hH]ydrological [iI]nstitute)\b',
        r'\b([mM]eteo[sW]wiss)\b',
        r'\b([cC]ambridge [uU]niversity [bB]otanic [gG]arden)\b']
    }
)

# 2019–20 Australian bushfire season
heat_tags_2020 = pd.DataFrame(
    {'tags': [
        r'\b([wW]ildfires?)\b',
        r'\b([oO]range sk(y|ies))\b',
        r'\b([sS]moke clouds?)\b',
        r'\b(([bB]ush)?[fF]ires?)\b',
        r'\b([mM]egafires?)\b',
        r'\b([bB]urning forests?)\b',
        r'\b(Black Summer)\b']
    }
)

# General tags for storms
storm_tags = pd.DataFrame(
    {'tags': [
        #r'\b([tT]ropical [sS]torms?)\b',
        #r'\b([cC]yclones?)\b',
        #r'\b([tT]yphoons?)\b',   # Maybe only include for typhoon?
        #r'\b([hH]urricanes?)\b', # Maybe only include for hurricane?
        r'\b([wW]inds?)\b',
        r'\b([gG]usts?)\b',
        r'\b((one|ten|[0-9]{1,2})-minute sustain(ed)?)\b',
        r'\b([mM]aximum sustained winds?)\b',
        r'\b([gG]ale[- ]force)\b',
        r'\b([wW]orld [mM]eteorological [oO]rganisation)\b',
        r'\b(WMO)\b']
    }
) 

# Hurricane Patricia Mexico
storm_tags_2015 = pd.DataFrame(
    {'tags': [
        r'\b([cC]yclones?)\b',
        r'\b([hH]urricanes?)\b',
        r'\b(Patricia)\b',
        r'\b([tT]ropical [sS]torms?)\b',
        r'\b([cC]ategory 5)\b',
        r'\b([fF]lood(waters?|s|ed|ing)?)\b',
        r'\b(rain(ed|s|fall)?)\b',
        r'\b(NOAA)\b',
        r'\b(Tehuantepec)\b',
        r'\b(Jalisco)\b',
        r'\b(Federal Emergency Management Agency|FEMA)\b',
        r'\b(National Hurricane Center|NHC)\b',
        r'\b(Mexican (Red Cross|Army|Navy|Federal Police))\b']
    }
) 

# Cyclone Winston Fiji
storm_tags_2016 = pd.DataFrame(
    {'tags': [
        r'\b([cC]yclones?)\b',
        r'\b(Winston)\b',
        r'\b([cC]ategory 5)\b',
        r'\b(Vanua Balavu)\b',
        r'\b(Viti Levu)\b',
        r'\b(Fiji)\b',
        r'\b([jJ]oint [tT]yphoon [wW]arning [cC]enter)\b',
        r'\b(Rakiraki District)\b',
        r'\b(FMS)\b',
        r'\b(Fijian Red Cross)\b']
    }
) 

# Hurricane Harvey USA
storm_tags_2017 = pd.DataFrame(
    {'tags': [
        r'\b([hH]urricanes?)\b',
        r'\b(Harvey)\b',
        r'\b([tT]ropical [sS]torms?)\b',
        r'\b([cC]ategory 4)\b',
        r'\b([fF]lood(waters?|s|ed|ing)?)\b',
        r'\b(rain(ed|s|fall)?)\b',
        r'\b(NOAA)\b',
        r'\b([sS]an [jJ]os[ée] [iI]sland)\b',
        r'\b(Holiday Beach)\b',
        r'\b(Federal Emergency Management Agency|FEMA)\b',
        r'\b(National Hurricane Center|NHC)\b',
        r'\b(H.R. ?601)\b']
    }
) 

# Pacific Asia Typhoon Mangkhut (Ompong) and Hurricane Florence in US 
storm_tags_2018 = pd.DataFrame(
    {'tags': [
        # Mangkhut tags
        r'\b([cC]yclones?)\b',
        r'\b([tT]yphoons?)\b',
        r'\b([mM]angkhut)\b',
        r'\b([oO]mpong)\b',
        r'\b([cC]agayan)\b',
        r'\b([cC]ategory 5)\b',
        r'\b([nN]orthern [mM]ariana [iI]slands)\b',
        r'\b([bB]aggao)\b',
        r'\b([cC]agayan)\b',
        r'\b([hH]ong [kK]ong [oO]bservatory)\b',
        r'\b([hH]urricane [sS]ignal)\b',
        r'\b([gG]uangdong)\b',
        r'\b([mM]eteorological [bB]ureau)\b',
        r'\b([gG]uangzhou)\b',
        ## Hurricane Florence tags
        r'\b([hH]urricanes?)\b',
        r'\b(Florence)\b',
        r'\b([tT]ropical [sS]torms?)\b',
        r'\b([cC]ategory 4)\b',
        r'\b([wW]rightsville [bB]each)\b',
        r'\b([fF]lood(waters?|s|ed|ing)?)\b',
        r'\b(rain(ed|s|fall)?)\b',
        r'\b(NOAA)\b',
        r'\b(SCEMD)\b',
        r'\b(Federal Emergency Management Agency|FEMA)\b',
        r'\b(National Hurricane Center|NHC)\b']
    }
)

# Japan Tropical Cyclone Hagibis
storm_tags_2019 = pd.DataFrame(
    {'tags': [
        r'\b([cC]yclones?)\b',
        r'\b([tT]yphoons?)\b',
        r'\b([rR]eiwa 1)\b',
        r'\b([hH]agibis)\b',
        r'\b([cC]ategory 5)\b',
        #r'\b([jJ]apan)\b', too broad
        r'\b([fF]lood(waters?|s|ed|ing)?)\b',
        r'\b([lL]andslides?)\b',
        r'\b(rain(ed|s|fall)?)\b',
        r'\b([cC]hikuma [rR]iver)\b',
        r'\b([uU]eda)\b',
        r'\b([hH]imawari)\b',
        r'\b([nN]agano)\b',
        r'\b([iI]chihara)\b',
        r'\b([sS]hinkansen)\b',
        r'\b([fF]ukushima)\b',
        r'\b([aA]kiyama [rR]iver)\b',
        r'\b([eE]vacuat(ion|ed?)( center)?)\b',
        r'\b([jJ]apan [mM]eteorological [aA]gency)\b',
        r'\b([iI]zu [pP]eninsula)\b',
        r'\b([sS]hizuoka)\b']
    }
)

# Tropical Cyclone Kammuri
storm_tags_2020 = pd.DataFrame(
    {'tags': [
        r'\b([cC]yclones?)\b',
        r'\b([tT]yphoons?)\b',
        r'\b([kK]ammuri)\b',
        r'\b([tT]isoy)\b',
        r'\b(Mariana Islands)\b',
        r'\b([cC]ategory 4)\b',
        r'\b(Philippine Area of Responsibility)\b',
        r'\b(Bicol Region)\b',
        r'\b(PAGASA)\b',
        r'\b([fF]lood(waters?|s|ed|ing)?)\b',
        r'\b(rain(ed|s|fall)?)\b']
    }
)

# Cyclone Amphan India Bangladesh
storm_tags_2020_unused = pd.DataFrame(
    {'tags': [
        r'\b([cC]yclones?)\b',
        r'\b(Amphan)\b',
        r'\b([cC]ategory 5)\b',
        r'\b(West Bengal)\b',
        r'\b(Kerala)\b',
        r'\b(Satkhira)\b',
        r'\b([jJ]oint [tT]yphoon [wW]arning [cC]enter)\b',
        r'\b(North Indian Ocean)\b',
        r'\b(Indian (Air Force|Navy))\b',
        r'\b(National Disaster Response Force|NDRF)\b',
        r'\b(Bangladesh (Air Force|Army|Armed Forces|Meteorological Department))\b',
        r'\b(Sri Lanka (Air Force|Navy))\b',
        r'\b([fF]lood(waters?|s|ed|ing)?)\b',
        r'\b([lL]andslides?)\b',
        r'\b(rain(ed|s|fall)?)\b']
    }
) 

climate_tags = pd.DataFrame(
    {'tags': [
        r'\b([cC]limate ([iI]mpact|[cC]hange|[cC]risis|[mM]odel|[eE]mergency))\b',
        r'\b([gG]lobal [wW]arming)\b',
        r'\b([gG]reenhouse)\b']
    }
) 