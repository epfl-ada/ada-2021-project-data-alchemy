# Influence of Natural Disasters on Climate Change Discussion

## Abstract

Climate change is a central issue in our world today and it has already had observable effects on the environment and rising temperatures are fueling environmental degradation through natural disasters and weather extremes. The consequences will become more and more devastating and will likely also reach irreversible highs. As young adults, these dire consequences are something that we become more and more prone to experiencing firsthand. The goal of this project is to determine how natural disaster occurrences influence the discussion around climate change. We would like to determine to what degree a particular natural disaster, such as a hurricane, sparks conversation around the topic of climate change. We would like to find out if the issue of climate change has become a more central topic over time as a result of natural disasters having potentially become increasingly severe.

## Research Questions

The main research question is :
- Do natural disasters influence the discussion around climate change? 

From there, multiple subquestions can be explored :

- Do certain natural disasters have a bigger influence than others? Is there a geographical link between the two, i.e., is there more discussion about climate change when natural distasters occur in specific regions rather than others? 
- Could we then estimate the impact that a hypothetical major tsunami in the United States would have on climate change discussions? 
- Have natural disasters generally become more and more severe over the last years in terms of number of casualties, duration or damages for example? If so, is there a significant correlation between the increased severity and the amount of attention climate change gets in the news? 
- Which indicators of a natural disaster have the biggest impact how much discussion there is about climate change, is it the death count, the damage cost or maybe some physical attribute of the disaster?
-What is the public sentiment towards climate change and natural disasters? Which natural disasters have the greatest impact on public sentiment? Has public sentiment towards climate change changed over time and what are the trends?

## Additional Datasets

### EM-DAT Database

EM-DAT is a database on natural and technological disasters, containing essential data on the occurrence and effects of more than 21,000 disasters in the world, from 1900 to present. EM-DAT is maintained by the Centre for Research on the Epidemiology of Disasters (CRED) at the School of Public Health of the Université catholique de Louvain located in Brussels, Belgium. 

A disaster has to conform to at least one of the following criteria:

- 10 or more people dead;
- 100 or more people affected;
- The declaration of a state of emergency
- A call for international assistance

Datasets can be extracted for free from the EM-DAT database for non-commercial purposes, such as ours. A dataset can be extracted according to specifications such as time intervals (startyear-endyear), disaster types and (sub)subtypes (Natural -> Meteorological -> Storm -> Tropical cyclone) and geographical location (continents, regions, countries). The datasets can only be downloaded as .xlsx files but can be converted to CSV using a [conversion](https://cloudconvert.com/xlsx-to-csv) tool. 

A retrieved dataset contains relevant information such as:
- Disaster type (hierarchy from Group to Subsubtype)
- Geographical location (Continent, Region, Country and specific locations such as cities/districts)
- Duration (start date - end date)
- Impact (deaths, injuries, number of affected, number of homeless, damages and reconstruction costs in USD$)

There is additional information such as physical attributes of the disaster (such as the are covered by a flood), aid contributions in USD$ and the source of the information. This data could serve a purpose in our project but it is quite sparse.

The dataset containing all natural disasters for all continents between 2015 and 2020 has 2164 entries contained in a CSV file of size 885KB.

## Methods (TODO)

First, we need to be able to accurately identify quotes that pertain to climate change. 
The first idea and also easiest one is to simply filter data by removing expressions we attribute to metaphors. That's what we do in the notebook filter_data.ipynb. 
We have tried using metaphor detection algorithms but have not been able to find one that was able to filter any quotes. In the subsequent project process, we will explore better filtering methods.

We also need to accurately identify what triggers discussion around climate change. For example, if there is a week-long climate change conference that sparks a lot of discussion around the topic but no major disaster has recently taken place, trying to make sense of the increase in discussion without any disaster could influence our analysis. No current database tracks these sorts of events. This problem can be dealt with by filtering out certain known events like the September 2019 climate strikes and by focusing on periods when major natural disasters are known to occur. In addition, we havce access to the EM-DAT database so we could look specifically at periods following a known disaster.

To process and examine the data, we have counted the occurences of the keywords and then performed a rolling average to smooth our data. Then, a simple cross correlation function shows significant correlation. 

In order to analyze public sentiment towards climate change and natural disasters, we give each quote a positive/negative score and subjective/objective score. 
This not only helps us analyze public sentiment changes and correlations, but also helps us filter out some irrelevant data. Test code of this part is in the sentiment-analysis folder, 
and we will integrate it into the process notebook during the subsequent project process.

Using EM-DAT database to classify natural disasters in terms of severity and region, and the number of discussions resulting from different regions and different levels of natural disaster severity were analysed separately and compared.
## Proposed Timeline

- Week 1 (next week): Initial data analysis
- Week 2: In-depth analysis (effects of different indicators etc..)
- Week 3: More analysis and maybe some regression (estimate effect of hypothetical disasters)
- Week 4: Add everything together
- Week 5 (submission week): Final Touches

## Internal Milestones (TODO)

- Peng
    - Area correlation analysis, Hypothetical experiments and analysis.
    - Analyse the impact of climate change on public sentiment，and the degree of impact of different natural 
      disasters on public sentiment，find the correlations.
- Colin
    - ...
    - ...
- Gil
    - Evaluate if certain disasters cause more discussion
    - Create skeleton of website

## Structure of Notebooks

The code is organised notebooks related to each step of the data analysis :

### extract_data.ipynb

Extract data from the json files. <br> 
This notebook will search for any quotes from a list of speakers containing any of the keywords in a list of keywords and write a binary pickle file containing the data.

### filter_data.ipynb

Filtering of false positives for certain keywords that are subject to metaphorical uses. 

### emdat.ipynb

Loading and cleaning of the dataset taken from the EM-DAT database.

### process.ipynb

Process data from both the Quotebank dataset as well as the EM-DAT dataset. Plot evolutions of discussion around topics and of the impacts of natural disasters.

### sentiment_test.py
Based on third party github repositories'TexyBlob' ,giving sentiment scores for quotes.


## Questions for TAs


 
--