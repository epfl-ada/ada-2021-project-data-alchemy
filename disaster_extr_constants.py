### -------- IMPORTS -----------------------------------------------------------------------------------------

import pandas as pd
from disaster_extr_helpers import extract_quotes_protected, extract_quotes

### ------------------ CONSTANTS -----------------------------------------------------------------------

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
# Not necessary to add to csv file, row already added to csv file
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

## TAGS USED FOR PROCESSING/FILTERING

heat_tags_2015_pos = pd.DataFrame(
    {'tags': [
        r'\b([iI]ndia)\b',
        r'\b(IMD)\b',
        r'\b([hH]eat[ -]?[wW]aves?)\b',
        r'\b(([hH]igh|[sS]evere|[eE]xtreme) temperatures?)\b',
        r'\b([cC]elsius|[fF]ahrenheit)\b',
        r'\b(([eE]xtreme|[vV]olatile) [wW]eather)\b',
        r'\b([hH]eat[ -]?strokes?)\b',
        r'\b([hH]eat[ -]?storms?)\b',
        r'\b([wW]orld [mM]eteorological [oO]rganisation)\b']
    }
)

heat_tags_2016_pos = pd.DataFrame(
    {'tags': [
        r'\b([iI]ndia)\b',
        r'\b(IMD)\b',
        r'\b([hH]eat[ -]?[wW]aves?)\b',
        r'\b(([hH]igh|[sS]evere|[eE]xtreme) temperatures?)\b',
        r'\b([cC]elsius|[fF]ahrenheit)\b',
        r'\b(([eE]xtreme|[vV]olatile) [wW]eather)\b',
        r'\b([hH]eat[ -]?strokes?)\b',
        r'\b([hH]eat[ -]?storms?)\b',
        r'\b([wW]orld [mM]eteorological [oO]rganisation)\b']
    }
)

heat_tags_2015_neg = pd.DataFrame(
    {'tags': [
        r'\b([aA]ustralia)\b',
        r'\b([rR]enault)\b',
        r'\b([cC]anada)\b',
        r'\b([fF]ahrenheit)\b',
        r'\b([wW]arm ([wW]elcome|[gG]reetings))\b',
        r'\b([wW]aste [hH]eat)\b',
        r'\b([nN]aked)\b',
        r'\b([rR]elations?)\b',
        r'\b([eE]l [nN]i[ñn]o)\b',
        r'\b([gG]ames?)\b',
        r'\b([cC]old?)\b',
        r'\b([rR]eceived)\b',
        r'\b(Europe)\b',
        r'\b(Everest)\b',
        r'\b(Honolulu)\b',
        r'\b([rR]elationships?)\b',
        r'\b([yY]oga?)\b',
        r'\b([rR]aces?)\b',
        r'\b([sS]tars?)\b',
        r'\b((3[- ]?D))\b',
        r'\b([vV]egetarians?)\b',
        r'\b([cC]owboys?)\b',
        r'\b([nN]anostructures?)\b',
        r'\b([iI]mmigrants?)\b',
        r'\b([dD]iseases?)\b',
        r'\b([pP]revious [rR]esearch)\b']
    }
)

heat_tags_2016_neg = pd.DataFrame(
    {'tags': [
        r'\b([aA]ustralian?)\b',
        r'\b(Vermont)\b'
        r'\b([rR]enault)\b',
        r'\b([cC]anada)\b',
        #r'\b([fF]ahrenheit)\b',
        r'\b([wW]arm ([wW]elcome|[gG]reetings))\b',
        r'\b([wW]aste [hH]eat)\b',
        r'\b([nN]aked)\b',
        r'\b([rR]elations?)\b',
        r'\b([eE]l [nN]i[ñn]o)\b',
        r'\b([gG]ames?)\b',
        r'\b([cC]old?)\b',
        r'\b([rR]eceived)\b',
        r'\b(Europe)\b',
        r'\b(Everest)\b',
        r'\b(Honolulu)\b',
        r'\b([rR]elationships?)\b',
        r'\b([yY]oga?)\b',
        r'\b([rR]aces?)\b',
        r'\b([sS]tars?)\b',
        r'\b((3[- ]?D))\b',
        r'\b([vV]egetarians?)\b',
        r'\b([cC]owboys?)\b',
        r'\b([nN]anostructures?)\b',
        r'\b([iI]mmigrants?)\b',
        r'\b([dD]iseases?)\b',
        r'\b([pP]revious [rR]esearch)\b',
        r'\b([sS]teams?)\b',
        r'\b([cC]annabis)\b',
        r'\b([pP]romises?)\b',
        r'\b([uU]nfriendly)\b',
        r'\b(9/11)\b',
        r'\b([pP]aris)\b',
        r'\b(Atlanta)\b',
        r'\b([sS]oil)\b',
        r'\b(180)\b',
        r'\b(451)\b',
        r'\b([fF]rosts?)\b',
        r'\b([cC]hina)\b',
        r'\b([rR]aspberr(ies|y))\b',
        r'\b(in here)\b',
        r'\b(Kelvin)\b',
        r'\b([eE]ast [cC]oast)\b',
        r'\b([nN]itrogen|[hH]elium)\b',
        r' -\d',
        r'\b(Fort McMurray)\b',
        r'\b([mM]ozzarella)\b',
        r'\b([sS]nowy?)\b',
        r'\b([hH]eated)\b',
        r'\b(\d [aApP][mM])\b', ## US time format
        r'\b([iI]nternet)',
        r'\b([pP]romotions?)\b',
        r'\b([lL]os [aA]ngeles|LA)\b',
        r'\b([aA]thletes?)\b',
        r'\b([pP]liocene)\b',
        r'\b([mM]editerranean)\b',
        r'\b((1|1\.5|2|2.5)[- ][dD]egrees?)\b',
        r'\b([iI]nfections?)\b',
        r'\b([hH]eat index)\b',
        r'\b([bB]oiling)\b',
        r'1.5',
        r'\b([mM]inus)\b',
        r'\b([tT]wo to four)\b',
        r'\b(Prices)\b',
        r'\b([bB]ottom(est)?)\b',
        r'\b([sS]olar)\b',
        r'\b([yY]ou need)\b',
        r'\b([cC]hemistry)\b',
        r'\b([hH]ostile)\b',
        r'\b([hH]ospitable)\b',
        r'\b(1000|600)\b',
        r'\b([cC]ell)\b',
        r'\b([vV]alery)\b',
        r'\b(two [dD]egrees?)\b',
        r'\b([oO]ffspring)\b',
        r'\b([fF]irefighters?)\b',
        r'\b([cC]omfort)\b',
        r'\b([vV]oltages?)\b',
        r'\b([hH]andle)\b',
        r'\b([hH]ighs)\b',
        r'\b([iI]ce[- ]cream)\b',
        r'\b([gG]rowth)\b',
        r'\b(Today)\b',
        r'!',
        r'\b([cC]ars)\b',
        r'\b(vehicle)\b',
        r'\b([cC]ompan(y|ies))\b',
        r'\b([dD]emands?)\b',
        r'\b([aA]greements?)\b',
        r'\b([pP]ollution)\b',
        r'\b([oO]utrageous)\b',
        r'\b([fF]unny)\b',
        r'\b([iI]nflation)\b',
        r'\b([fF]ake)\b',
        r'\b([cC]ommerce)\b',
        r'\b([kK]inds?)\b',
        r'\b([gG]racious(ly)?)\b',
        r'\b(Americans?)\b',
        r'\b(U.?S.?|United States)\b',
        r'\b(Oregon)\b',
        r'\b([cC]oming decades?)\b',
        r'\b(alpine)\b',
        r'\b([tT]exas)\b',
        r'\b(blasts?)\b',
        r'\b([oO]ils?)\b',
        r'\b([mM]atch(es)?)\b',
        r'\b([fF]ish)\b',
        r'\b([sS]torms?)\b',
        r'\b([hH]urricanes?)\b']
    }
)

heat_tags_2017_pos = pd.DataFrame(
    {'tags': [
        r'\b([hH]eat[ -]?[wW]aves?)\b',
        r'\b(([hH]igh|[sS]evere|[eE]xtreme) temperatures?)\b',
        r'\b([cC]elsius|[fF]ahrenheit)\b',
        r'\b(([eE]xtreme|[vV]olatile) [wW]eather)\b',
        r'\b([hH]eat[ -]?strokes?)\b',
        r'\b([hH]eat[ -]?storms?)\b',
        r'\b(Pilliga)\b',
        r'\b(Talleganda)\b',
        r'\b(Queensland Ambulance Service)\b',
        r'\b([wW]ildfires?)\b',
        r'\b([oO]range sk(y|ies))\b',
        r'\b([sS]moke clouds?)\b',
        r'\b([bB]ush[- ]?[fF]ires?)\b',
        r'\b([mM]egafires?)\b',
        r'\b([bB]urning (forests?|bush(es)?|areas?|wildlife|lands?))\b',
        r'\b([sS]ir [iI]van)\b',
        r'\b([fF]ires? (burn(ed|ing)?|alerts?))\b',
        r'\b([fF]lames?)\b'
        r'\b(Taree)\b',
        r'\b(Ivanhoe)\b'
    ]
    }
)

# Forgot to save and extremely time-consuming to create list
# so decided not to redo whole procedure
heat_tags_2017_neg = heat_tags_2016_neg

heat_tags_2018_pos = pd.DataFrame(
    {'tags': [
        r'\b([jJ]apan)\b',
        r'\b([hH]eat[ -]?[wW]aves?)\b',
        r'\b(([hH]igh|[sS]evere|[eE]xtreme) temperatures?)\b',
        r'\b(([eE]xtreme|[vV]olatile) [wW]eather)\b',
        r'\b([hH]eat[ -]?strokes?)\b',
        r'\b([hH]eat[ -]?storms?)\b',
        r'\b([bB]ureau [oF]f [mM]eteorology)\b',
        r'\b(Korea)\b',
        r'\b([jJ]apan [mM]eteorological [aA]gency)\b',
        r'\b([tT]okyo [fF]ire [dD]epartment)\b',
    ]
    }
)

heat_tags_2018_neg = pd.DataFrame(
    {'tags': [
        r'\b([tT]ongues?)\b',
        r'\b([tT]urkey)\b',
        r'\b([gG]ames?)\b',
        r'\b([bB]usiness(es)?)\b',
        r'\b([pP]layers?)\b',
        r'\b([sS]tudios?)\b',
        r'\b([hH]elmets?)\b',
        r'\b([bB]ars?)\b',
        r'\b(Arkansas)\b',
        r'\b(Obama)\b',
        r'\b([vV]iolences?)\b',
        r'\b([fF]all)\b',
        r'\b(Chicago(ans?)?)\b',
        r'\b([cC]redits?)\b',
        r'\b([gG]angs?)\b',
        r'\b([sS]ales?)\b',
        r'\b([hH]ousing)\b',
        r'\b([bB]lokes?)\b',
        r'\b([sS]hadows?)\b',
        r'\b([hH]oneys?)\b',
        r'\b([tT]obacco)\b',
        r'\b([lL]aps?)\b',
        r'\b([sS]now)\b',
        r'\b([vV]isas?)\b',
        r'\b([cC]hills?)\b',
        r'\b(Canada)\b',
        r'\b([rR]eactors?)\b',
        r'\b([cC]lients?)\b',
        r'\b([rR]ock)\b',
        r'\b(bizarre)\b',
        r'\b([iI]mmune)\b',
        r'\b([eE]urope)\b',
        r'\b([cC]haracters?)\b',
        r'\b([mM]edals?)\b',
        r'\b([tT]rades?)\b',
        r'\b([gG]overnments?)\b',
        r'\b([iI]ndia(ns)?)\b',
        r'\b(Australia)\b',
        r'\b([tT]rails?)\b',
        r'\b(UK)\b',
        r'\b(Scotland)\b',
        r'\b([oO]ceans?)\b',
        r'\b([rR]osters?)\b',
        r'BlockchainDome',
        r'\b([cC]hurch(es)?)\b',
        r'\b([rR]esearch)\b',
        r'\b([mM]ontreal)\b',
        r'2000',
        r'\b(North Korea)\b',
        r'\b([bB]illboard)\b',
        r'\b([iI]rons?)\b',
        r'\b([wW]inds?)\b',
        r'\b([mM]arines?)\b']
    }
)

# Apply extra step (based on url contents)
def heat_2018_extra(filtered_for_pos_then_neg):
    filtered_extra = extract_quotes_protected(
        filtered_for_pos_then_neg, 
        r'\b([wW]orld|[rR]ecords?|[gG]lobal|[jJ]apan)\b', 
        r'fire|\b(England)\b|\b(California)\b',
        with_url=[r'[jJ]ap|tok|korea|china', 'urls', r'http', 'urls']
        )
    return filtered_extra
    

heat_tags_2019_pos = pd.DataFrame(
    {'tags': [
        r'\b([hH]eat[ -]?[wW]aves?)\b',
        r'\b(([hH]igh|[sS]evere|[eE]xtreme|[rR]ecord[- ][bB]reaking) temperatures?)\b',
        r'\b([cC]elsius|[fF]ahrenheit)\b',
        #r'\b(([eE]xtreme|[vV]olatile) [wW]eather)\b',
        r'\b([hH]eat[ -]?strokes?)\b',
        r'\b([hH]eat[ -]?storms?)\b',
        r'\b([sS]corching)\b'
    ]
    }
)

heat_tags_2019_neg = pd.DataFrame(
    {'tags': [
        r'\b([tT]ongues?)\b',
        r'\b([tT]urkey)\b',
        r'\b([gG]ames?)\b',
        #r'\b([bB]usiness(es)?)\b',
        r'\b([pP]layers?)\b',
        r'\b([sS]tudios?)\b',
        r'\b([hH]elmets?)\b',
        #r'\b([bB]ars?)\b',
        r'\b(Arkansas)\b',
        #r'\b(Obama)\b',
        r'\b([vV]iolences?)\b',
        r'\b([fF]all)\b',
        r'\b(Chicago(ans?)?)\b',
        r'\b([cC]redits?)\b',
        r'\b([gG]angs?)\b',
        r'\b([sS]ales?)\b',
        r'\b([hH]ousing)\b',
        r'\b([bB]lokes?)\b',
        r'\b([sS]hadows?)\b',
        r'\b([hH]oneys?)\b',
        r'\b([tT]obacco)\b',
        r'\b([lL]aps?)\b',
        #r'\b([sS]now)\b',
        r'\b([pP]aris ([cC]limate ([cC]hange )?)?[aA]greements?)\b',
        r'\b([pP]aris (([gG]lobal )?[cC]limate )?[aA]ccords?)\b',
        r'\b(Missouri)\b',
        r'\b(wartime)\b',
        r'\b([dD]inners?)\b',
        r'\b([iI]ndustr(y|ies))\b',
        r'\b(Boston)\b',
        r'\b(EU)\b',
        r'\b(Canada)\b',
        r'\b(United States|U.?S.?)\b',
        r'\b([bB]ananas?)\b'
        r'\b([sS]treets?)\b',
        r'\b([tT]ackles?)\b',
        r'\b([qQ]uickly)\b',
        r'\b([pP]reventable)\b',
        r'\b([cC]andidates?)\b',
        r'\b([mM]usic)\b',
        r'\b([rR]omances?)\b',
        r'\b([mM]arines?)\b',
        r'\b([tT]urns? up)\b',
        r'\b([pP]lay(ers?)?)\b',
        r'\b(Pirelli)\b',
        r'\b(Mercedes-Benz)\b',
        r'\b([cC]lassrooms?)\b',
        r'\b(New York(ers?)?)\b',
        r'\b(([tT]wo|[oO]ne) degrees?)\b',
        r'\b([mM]inus|[nN]egative)\b',
        r'\b([sS]hops?)\b',
        r'\b(MTA)\b',
        

        

        r'\b([rR]eactors?)\b',
        r'\b([cC]lients?)\b',
        r'\b([rR]ock)\b',
        r'\b([bB]eers?)\b',
        r'\b([lL]ovely)\b',
        r'\b([aA]dministrations?)\b',
        r'\b([pP]ets?)\b',
        r'\b([jJ]ew(s|ish))\b',
        r'\b([mM]edical(ly)?)\b',
        r'\b([wW]arm[- ]?ups?)\b',
        r'\b([hH]omeless(ness)?)\b',
        r'\b(New[- ]?England)\b',
        r'\b([dD]oors?)\b',
        r'\b([bB]at(sm[ea]n)?)\b',
        r'\b([hH]and warmers?)\b',
        r'\b([fF]reezing)\b',
        r'\b(Japan)\b',
        r'\b((1|1\.5|2|2\.5) degrees?)\b',
        r'\b(20(20|30|40))\b',
        r'\b(Mars)\b',
        r'\b([cC]oldest)\b',
        r'\b([fF]rozen?)\b',
        r'\b([hH]umid(ity)?)\b',
        r'\b([vV]olcano(es?)?)\b',
        r'\b(corridor)\b',
        r'\b([cC]ores?)\b',
        r'\b([lL]ow temperatures?)\b',
        r'\b([iI]nternal)\b',
        r'\b([iI]nsane)\b',
        r'\b([aA]thletes?)\b',

        


        r'\b([rR]osters?)\b',
        r'\b([sS]tud(y|ies))\b',
        r'\b(America(ns?)?)\b',
        r'\b([rR]ules?)\b',
        r'\b([sS]ediments?)\b',
        r'\b([sS]eriously)\b',
        r'\b([tT]heor(y|etical))\b',
        r'\b([eE]xperiment(s|al|ally)?)\b',
        r'\b([hH]eat cramps?)\b',
        r'\b([pP]izzas?)\b',
        r'\b([rR]ails?)\b',
        r'\b(NYPD)\b',
        r'\b([dD]roughts?)\b',

    ]
    }
)

def heat_2019_extra(filtered_for_pos_then_neg):
    filtered_for_pos_then_neg = extract_quotes(
        filtered_for_pos_then_neg, 
        r'-us-|-america-|united-states|kupwara|bihar|[iI]owa|us-news|moon|delhi|tree|friend|houston|atlanta|arkansas|cars|america|football|mitch-petrus|new-jersey|artwork|clauson|chandrayaan|outback|manila|sydney|food|burger|boston|connecticut|cali|cleveland|woodstock|kspr|county|/us/|nyc|blackout|phil|syracuse', 
        field='urls', 
        complement=True)
    return filtered_for_pos_then_neg

heat_tags_2020_pos = pd.DataFrame(
    {'tags': [
        r'\b([bB]ush [fF]ires?)\b',
        r'(?=.*\b(Australia)\b)(?=.*\b([tT]emperatures?)\b)',
        r'(?=.*\b(Australia)\b)(?=.*\b([fF]ires?)\b)',
        r'(?=.*\b(Australia)\b)(?=.*\b([hH]eat[ -]?[wW]aves?)\b)',
        r'(?=.*\b(Sydney|New South Wales|Melbourne)\b)(?=.*\b([hH]eat[ -]?[wW]aves?)\b)'
    ]
    }
)

heat_tags_2020_neg = pd.DataFrame(
    {'tags': [
        r'\b([tT]ongues?)\b',
        r'\b([tT]urkey)\b',
        r'\b([gG]ames?)\b',
        r'\b([pP]layers?)\b',
        r'\b([sS]tudios?)\b',
        r'\b([hH]elmets?)\b',
        r'\b(Arkansas)\b',
        r'\b([vV]iolences?)\b',
        r'\b([fF]all)\b',
        r'\b(Chicago(ans?)?)\b',
        r'\b([cC]redits?)\b',
        r'\b([gG]angs?)\b',
        r'\b([sS]ales?)\b',
        r'\b([hH]ousing)\b',
        r'\b([bB]lokes?)\b',
        r'\b([sS]hadows?)\b',
        r'\b([hH]oneys?)\b',
        r'\b([tT]obacco)\b',
        r'\b([lL]aps?)\b',
        r'\b([pP]aris ([cC]limate ([cC]hange )?)?[aA]greements?)\b',
        r'\b([pP]aris (([gG]lobal )?[cC]limate )?[aA]ccords?)\b',
        r'\b(Missouri)\b',
        r'\b(wartime)\b',
        r'\b([dD]inners?)\b',
        r'\b([iI]ndustr(y|ies))\b',
        r'\b(Boston)\b',
        r'\b(EU)\b',
        r'\b(Canada)\b',
        r'\b(United States|U.?S.?)\b',
        r'\b([bB]ananas?)\b'
        r'\b([sS]treets?)\b',
        r'\b([tT]ackles?)\b',
        r'\b([qQ]uickly)\b',
        r'\b([pP]reventable)\b',
        r'\b([cC]andidates?)\b',
        r'\b([mM]usic)\b',
        r'\b([rR]omances?)\b',
        r'\b([mM]arines?)\b',
        r'\b([tT]urns? up)\b',
        r'\b([pP]lay(ers?)?)\b',
        r'\b(Pirelli)\b',
        r'\b(Mercedes-Benz)\b',
        r'\b([cC]lassrooms?)\b',
        r'\b(New York(ers?)?)\b',
        r'\b(([tT]wo|[oO]ne) degrees?)\b',
        r'\b([mM]inus|[nN]egative)\b',
        r'\b([sS]hops?)\b',
        r'\b(MTA)\b',
        r'\b(Europe)\b',
        r'\b(London)\b',
        r'\b(Paris)\b',
        r'\b(Belgium)\b',
        r'\b(France)\b',
        r'\b(Germany)\b',
        r'\b(Luxembourg)\b',
        r'\b(Netherlands)\b',
        r'\b(England)\b',
        r'\b([mM][ée]t[ée]o [fF]rance)\b',
        r'\b([gG]allargues-le-[mM]ontueux)\b',
        r'\b([bB]erlin[- ][tT]empelhof)\b',
        r'\b([bB]randenburg)\b',

        

        r'\b([rR]eactors?)\b',
        r'\b([cC]lients?)\b',
        r'\b([rR]ock)\b',
        r'\b([bB]eers?)\b',
        r'\b([lL]ovely)\b',
        r'\b([aA]dministrations?)\b',
        r'\b([pP]ets?)\b',
        r'\b([jJ]ew(s|ish))\b',
        r'\b([mM]edical(ly)?)\b',
        r'\b([wW]arm[- ]?ups?)\b',
        r'\b([hH]omeless(ness)?)\b',
        r'\b(New[- ]?England)\b',
        r'\b([dD]oors?)\b',
        r'\b([bB]at(sm[ea]n)?)\b',
        r'\b([hH]and warmers?)\b',
        r'\b([fF]reezing)\b',
        r'\b(Japan)\b',
        r'\b((1|1\.5|2|2\.5) degrees?)\b',
        r'\b(20(20|30|40))\b',
        r'\b(Mars)\b',
        r'\b([cC]oldest)\b',
        r'\b([fF]rozen?)\b',
        r'\b([hH]umid(ity)?)\b',
        r'\b([vV]olcano(es?)?)\b',
        r'\b(corridor)\b',
        r'\b([cC]ores?)\b',
        r'\b([lL]ow temperatures?)\b',
        r'\b([iI]nternal)\b',
        r'\b([iI]nsane)\b',
        r'\b([aA]thletes?)\b',

        


        r'\b([rR]osters?)\b',
        r'\b([sS]tud(y|ies))\b',
        r'\b(America(ns?)?)\b',
        r'\b([rR]ules?)\b',
        r'\b([sS]ediments?)\b',
        r'\b([sS]eriously)\b',
        r'\b([tT]heor(y|etical))\b',
        r'\b([eE]xperiment(s|al|ally)?)\b',
        r'\b([hH]eat cramps?)\b',
        r'\b([pP]izzas?)\b',
        r'\b([rR]ails?)\b',
        r'\b(NYPD)\b',
        r'\b([dD]roughts?)\b',

    ]
    }
)

storm_tags_2015_pos = pd.DataFrame(
    {'tags': [
        r'(?=.*\b([mM]exic(o|ans?)|[tT]ehuantepec|[cC]oasts?|[jJ]alisco)\b)(?=.*\b([hH]urricanes?|[sS]torms?)\b)',
        r'(?=.*\b([mM]exic(o|ans?)|[tT]ehuantepec|[cC]oasts?|[jJ]alisco)\b)(?=.*\b([fF]lood(waters?|s|ed|ing)?|[rR]ain(ed|s|fall)?|[lL]andslides?)\b)',
        r'\b(Patricia)\b',
        r'\b([cC]ategory 5)\b',
        r'\b(NOAA)\b',
        r'\b(National Hurricane Center|NHC)\b',
        r'\b(Mexican (Red Cross|Army|Navy|Federal Police))\b']
    }
)

def storm_tags_2015_extra(filtered_for_pos):
    filtered_extra = extract_quotes_protected(
        filtered_for_pos, 
        r'\b(Texas|Mexic(o|ans?)|[hH]urricanes?|[cC]ategory|[sS]torms?)\b', 
        r'\b(Patricia|)\b',
        #with_url=[r'\.co\.uk', 'urls', r'http', 'urls']
    )
    return filtered_extra

storm_tags_2016_pos = pd.DataFrame(
    {'tags': [
        ## Hurricane Harvey tags
        r'(?=.*\b([fF]iji)\b)(?=.*\b([fF]lood(waters?|s|ed|ing)?|[rR]ain(ed|s|fall)?|[lL]andslides?|[cC]yclones?|[sS]torms?)\b)',
        r'\b(Winston)\b',
        r'\b(Vanua Balavu)\b',
        r'\b([cC]ategory 5)\b',
        r'\b(Fiji(an)?)\b',
        r'\b([jJ]oint [tT]yphoon [wW]arning [cC]enter)\b',
        r'\b(Rakiraki District)\b',
        r'\b(FMS)\b']
    }
)

storm_tags_2017_pos = pd.DataFrame(
    {'tags': [
        ## Hurricane Harvey tags
        r'(?=.*\b([tT]exas|[lL]ouisiana|[cC]oasts?|U.?S.?A?|[bB]each(es)?)\b)(?=.*\b([rR]ain(ed|s|fall)?|[lL]andslides?)\b)',
        r'(?=.*\b([tT]exas|[lL]ouisiana|[cC]oasts?|U.?S.?A?|[bB]each(es)?)\b)(?=.*\b([hH]urricanes?|[sS]torms?)\b)',
        r'(?=.*\b([tT]exas|[lL]ouisiana|[cC]oasts?|U.?S.?A?)\b)(?=.*\b([fF]lood(waters?|s|ed|ing)?|[rR]ain(ed|s|fall)?)\b)',
        r'\b(Harvey)\b',
        r'\b([cC]ategory 4)\b',
        r'\b([sS]an [jJ]os[ée] [iI]sland)\b',
        r'\b(H.R. ?601)\b',
        r'\b(NOAA)\b',
        r'\b(Federal Emergency Management Agency|FEMA)\b',
        r'\b(National Hurricane Center|NHC)\b']
    }
)

storm_tags_2018_pos_asia = pd.DataFrame(
    {'tags': [
        # Mangkhut tags
        r'(?=.*\b([cC]hin(a|ese)?|[pP]hilippines?|[hH]ong [kK]ong|[gG]uangdong|[gG]uangzhou|[cC]agayan|[bB]aggao|[aA]sian?)\b)(?=.*\b([rR]ain(ed|s|fall)?|[lL]andslides?)\b)',
        r'(?=.*\b([cC]hin(a|ese)?|[pP]hilippines?|[hH]ong [kK]ong|[gG]uangdong|[gG]uangzhou|[cC]agayan|[bB]aggao|[aA]sian?)\b)(?=.*\b([hH]urricanes?|[sS]torms?|[cC]yclones?|[tT]yphoons?)\b)',
        r'\b([mM]angkhut)\b',
        r'\b([oO]mpong)\b',
        r'\b([cC]ategory 5)\b',
        r'\b([nN]orthern [mM]ariana [iI]slands)\b',
        r'\b([hH]ong [kK]ong [oO]bservatory)\b',
        r'\b([hH]urricane [sS]ignal)\b',
        r'\b([mM]eteorological [bB]ureau)\b']
    }
)
        
storm_tags_2018_pos_america = pd.DataFrame(
    {'tags': [
        ## Hurricane Florence tags
        r'(?=.*\b([cC]ape [vV]erde|[cC]oasts?|U.?S.?A?|[cC]arolinas?|[bB]each(es)?|[vV]irginia|[mM]aryland|[gG]eorgia)\b)(?=.*\b([rR]ain(ed|s|fall)?|[lL]andslides?)\b)',
        r'(?=.*\b([cC]ape [vV]erde|[cC]oasts?|U.?S.?A?|[cC]arolinas?|[bB]each(es)?|[vV]irginia|[mM]aryland|[gG]eorgia)\b)(?=.*\b([hH]urricanes?|[sS]torms?)\b)',
        r'(?=.*\b([cC]ape [vV]erde|[cC]oasts?|U.?S.?A?|[cC]arolinas?|[bB]each(es)?|[vV]irginia|[mM]aryland|[gG]eorgia)\b)(?=.*\b([hH]urricanes?|[sS]torms?)\b)',
        r'(?=.*\b([cC]ape [vV]erde|[cC]oasts?|U.?S.?A?|[cC]arolinas?|[bB]each(es)?|[vV]irginia|[mM]aryland|[gG]eorgia)\b)(?=.*\b([fF]lood(waters?|s|ed|ing)?|[rR]ain(ed|s|fall)?)\b)',
        r'\b(Florence)\b',
        r'\b([cC]ategory 4)\b',
        r'\b(NOAA)\b',
        r'\b(SCEMD)\b',
        r'\b(Federal Emergency Management Agency|FEMA)\b',
        r'\b(National Hurricane Center|NHC)\b']
    }
)

storm_tags_2019_pos = pd.DataFrame(
    {'tags': [
        r'\b([hH]agibis)\b',
        r'\b([cC]ategory 5)\b',
        r'\b([rR]eiwa 1)\b',
        r'(?=.*\b([jJ]apan(ese)?|[iI]zu|[cC]hikuma|[uU]eda|[nN]agano|[sS]hinkansen|[fF]ukushima|[aA]sian?)\b)(?=.*\b([rR]ain(ed|s|fall)?|[lL]andslides?)\b)',
        r'(?=.*\b([jJ]apan(ese)?|[iI]zu|[cC]hikuma|[uU]eda|[nN]agano|[sS]hinkansen|[fF]ukushima|[aA]sian?)\b)(?=.*\b([hH]urricanes?|[sS]torms?|[cC]yclones?|[tT]yphoons?)\b)',
        r'(?=.*\b([jJ]apan(ese)?|[iI]zu|[cC]hikuma|[uU]eda|[nN]agano|[sS]hinkansen|[fF]ukushima)\b)(?=.*\b([dD]estructions?|[sS]tate of)\b)',
        r'(?=.*\b([jJ]apan(ese)?|[iI]zu|[cC]hikuma|[uU]eda|[nN]agano|[sS]hinkansen|[fF]ukushima)\b)(?=.*\b([fF]lood(waters?|s|ed|ing)?|[eE]vacuat(ion|ed?)( center)?)\b)'
    ]
    }
)

storm_tags_2020_pos = pd.DataFrame(
    {'tags': [
        r'\b([kK]ammuri)\b',
        r'\b([tT]isoy)\b',
        r'\b(PAGASA)\b',
        r'(?=.*\b([pP]hilippines?|Manila|Quezon|Davao|Caloocan|Budta|[aA]sian?)\b)(?=.*\b(rain(ed|s|fall)?)\b)',
        r'(?=.*\b([pP]hilippines?|Manila|Quezon|Davao|Caloocan|Budta|[aA]sian?)\b)(?=.*\b([hH]urricanes?|[sS]torms?|[cC]yclones?|[tT]yphoons?)\b)',
        r'(?=.*\b([pP]hilippines?|Manila|Quezon|Davao|Caloocan|Budta)\b)(?=.*\b([dD]estructions?|[sS]tate of)\b)',
        r'(?=.*\b([pP]hilippines?|Manila|Quezon|Davao|Caloocan|Budta)\b)(?=.*\b([fF]lood(waters?|s|ed|ing)?)\b)'
    ]
    }
)

### TEST

# General tags for heat waves
heat_tags_2015_neg_TEST = pd.DataFrame(
    {'tags': [
        r'\b([mM]ood)\b',
        r'\b([tT]oddler)\b',
        r'\b([vV]ehicle)\b',
        r'\b([cC]elebrate)\b',
        #r'\b([uU]niversity)\b',
        r'\b([dD]iplomas?)\b',
        r'\b([mM]useums?)\b',
        r'\b([aA]cademi(c|a))\b',
        r'\b([BM]A|[BM][sS][cC])\b',
        r'\b([sS]tudents?)\b',
        r'\b([cC]olleges?)\b',
        r'\b([eE]ducation)\b',
        r'\b([eE]quine)\b',
        r'\b([gG]raduates?)\b',
        r'\b(([uU]nder|[pP]ost)?graduate(\'s)? degrees?)\b',
        r'\b(([dD]esign|[cC][sS]|[sS]cience|[aA]dvanced|[fF]ake|[lL]aw|[uU]niversity) degrees?)\b',
        r'\b(([gG]rant|[cC]ollege|[hH]igher|[fF]or|[yY]ear|[aA]|[gG]et|[mM]y) degrees?)\b',
        r'\b(([hH]is|[hH]er|[tT]heir|[oO]ur) degrees?)\b',
        r'\b(([bB]achelor|[mM]aster)(\'?s)? degrees?)\b',
        r'\b([wW]arm-hearted)\b',
        r'\b([nN]ominat(ion|ed))\b',
        r'\b([cC]harming)\b',
        r'\b([cC]omedy)\b',
        r'\b([mM]eat)\b',
        r'\b([tT]acos)\b',
        r'\b([hH]ottest issues?)\b',
        r'\b([rR]estaurants?)\b',
        r'\b([aA]leppo)\b',
        r'\b([iI]ran(ians?)?)\b',
        r'\b([tT]roops?)\b',
        r'\b([iI]raq(i|is)?)\b',
        r'\b(Afghanistan(is?)?)\b',
        r'\b(heat on it)\b',
        r'\b([gG]oalie)\b',
        r'\b([sS]hots)\b',
        r'\b([rR]acing)\b',
        r'\b([tT][yi]res?)\b',
        r'\b([pP]erfect storm)\b',
        r'\b([dD]ivorc(ing|e))\b',
        r'\b([gG]irlfriend)\b',
        r'\b([bB]oyfriend)\b',
        r'\b([tT]eachers?)\b',
        r'\b([the heat out of)\b',
        r'\b([hH]eating systems?)\b',
        r'\b(I live for)\b',
        r'\b([hH]ot-tempered)\b',
        r'\b([rR]ookies?)\b',
        r'\b([bB]asketballs?)\b',
        r'\b([bB]aseballs?)\b',
        r'\b(NBA)\b',
        r'\b([qQ]uarterbacks?)\b',
        r'\b([hH]is first years?)\b',
        r'\b([pP]lay(ed)? well)\b',
        r'\b([hH]ot-button)\b',
        r'\b(bands?)\b',
        r'\b([nN]utritionists?)\b',
        r'\b([pP]roduction loss(es)?)\b',
        r'\b(Miami Heat)\b',
        r'\b([sS]noop)\b',
        r'\b([hH]ot[- ](dogs?|toned|pants))\b',
        r'\b([hH]ot[- ](lunch(es)?|foods?|dinners?|breakfast|meals?|Springs|baths?|appetizers?|stove|energy))\b',
        r'\b([hH]ot[- ](gazes?|desires?|kiss(es)?|air balloons?|tea|touch|showers?|butter|plates?|cars?))\b',
        r'\b([sS]mokin\' hot)\b',
        r'\b(the lead)\b',
        r'\b([cC]rampons)\b',
        r'\b([wW]et basements?)\b',
        r'\b([hH]eat is on)\b',
        r'\b([sS]cams?)\b',
        r'\b(Market)\b',
        r'\b(Damascus)\b',
        r'\b(Homs)\b',
        r'\b([hH]ot on the)\b',
        r'\b([wW]arm[- ]up)\b',
        r'\b([pP]lay(ing|ers?|ed))\b',
        r'\b(iron)\b',
        r'\b([hH]ot-toned)\b',
        r'\b([mM]elodic)\b',
        r'\b([fF]unk)\b',
        r'\b([gG]uitars?)\b',
        r'\b([rR]hythms?)\b',
        r'\b([hH]ip[- ]hop)\b',
        r'\b([lL]yrics)\b',
        r'\b([tT]hirst for money)\b',
        r'\b(([fF]irst|[sS]econd|[tT]hird|[fF]ourth|[fF]ifth) heats?)\b',
        r'\b(steering)\b',
        r'\b(([wWhH]e(\'re|\'s)) get(s|tin(\'|g))? hot)\b',
        r'\b(room temperature)\b',
        r'\b([lL]imelight)\b',
        r'\b([mM]emories)\b',
        r'\b([wW]arm(est)? (welcome|thanks))\b',
        r'\b([uU]mpire)\b',
        r'\b([bB]alls?)\b',
        r'\b([sS]ports?)\b',
        r'\b([sS]ales?)\b',
        r'\b([sS]ex(ual))\b',
        r'\b(offices?)\b',
        r'\b([dD]egrees? (burns?|of|are|certifcates?|affix(es)?|(to the )?(left|right)|removed|were (faked?|fabricated)))\b',
        r'\b(verification of degrees?)\b',
        r'\b((45|90180|360|270|460)[- ]degrees?)\b',
        r'\b(([vV]arying) degrees?)\b',
        r'\b([lL]ove)\b',
        r'\b([cC]ounselors?)\b',
        r'\b([rR]ap(e|ists?))\b',
        r'\b([fF]resh(ness)?)\b',
        r'\b([mM]anagers?)\b',
        r'\b([bB]usiness(es)?)\b',
        r'\b([rR]otate(d|s)?)\b',
        r'\b([qQ]ualifications?)\b',
        r'\b([mM]arkets?)\b',
        r'\b([cC]omputers?)\b',
        r'\b([sS]creens?)\b',
        r'\b([cC]lass(es)?)\b',
        r'\b([pP]ayments?)\b',
        r'\b([bB]eers?)\b',
        r'\b([wW]ines?)\b',
        r'\b([eE]nglish)\b',
        r'\b([lL]iterature)\b',
        r'\b([sS]ymbolism)\b',
        r'\b([fF]reez(e|ing))\b',
        r'\b([cC]rowns?)\b',
        r'\b([cC]ocky)\b',
        r'\b([wW]orthless)\b',
        r'\b([cC]areers?)\b',
        r'\b([jJ]obs?)\b',
        r'\b([cC]ars?)\b',
        r'\b([tT]rains?)\b',
        r'\b([sS]lopes?)\b',
        r'\b([rR]aces?)\b',
        r'\b([yY]oga)\b',
        r'\b([mM]usic)\b',
        r'\b([hH]omosexuals?)\b',
        r'\b([hH]ell|HELL)\b',
        r'\b([hH]ibernate)\b',
        r'\b([sS]alt)\b',
        r'\b([fF]ishing)\b',
        r'\b([gG]irls?|[bB]oys?)\b',
        r'\b([jJ]ump(ing|s)?)\b',
        r'\b([fF]orged?)\b', 
        #r'\b([]eat)\b',

]
    }
)