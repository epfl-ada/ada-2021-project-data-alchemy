# **Influence of Natural Disasters on Climate Change Discussion**

## **Abstract**

Climate change is a central issue in our world today and it has already had observable effects on the environment and rising temperatures are fueling environmental degradation through natural disasters and weather extremes. The consequences will become more and more devastating and will likely also reach irreversible highs. As young adults, these dire consequences are something that we become more and more prone to experiencing firsthand. The goal of this project is to determine how natural disaster occurrences influence the discussion around climate change. We would like to determine to what degree a particular natural disaster, such as a hurricane, sparks conversation around the topic of climate change. We would like to find out if the issue of climate change has become a more central topic over time as a result of natural disasters having potentially become increasingly severe.

## **Research Questions**

The main research question is :
- **Do natural disasters influence the discussion around climate change?**

From there, multiple subquestions can be explored :

- Do certain natural disasters have a bigger influence than others? Is there a geographical link between the two, i.e., is there more discussion about climate change when natural distasters occur in specific regions rather than others? 
- Could we then estimate the impact that a hypothetical major tsunami in the United States would have on climate change discussions? 
- Have natural disasters generally become more and more severe over the last years in terms of number of casualties, duration or damages for example? If so, is there a significant correlation between the increased severity and the amount of attention climate change gets in the news? 
- Which indicators of a natural disaster have the biggest impact how much discussion there is about climate change ?
- What is the public sentiment towards climate change and natural disasters? Which natural disasters have the greatest impact on public sentiment? Has public sentiment towards climate change changed over time and what are the trends?

## **Additional Datasets**

### **EM-DAT Database**

EM-DAT is a database on natural and technological disasters, containing essential data on the occurrence and effects of more than 21,000 disasters in the world, from 1900 to present. EM-DAT is maintained by the Centre for Research on the Epidemiology of Disasters (CRED) at the School of Public Health of the Université catholique de Louvain located in Brussels, Belgium. 

A retrieved dataset contains relevant information such as:
- Disaster type
- Geographical location 
- Duration 
- Impact (deaths, injuries, number of affected, etc.)

The dataset containing all natural disasters for all continents between 2015 and 2020 has 2164 entries contained in a CSV file of size 885KB.

## **Methods**

First, we need to be able to accurately identify quotes that pertain to climate change. 
The first idea and also easiest one is to simply filter data by removing expressions we attribute to metaphors. That's what we do in the notebook filter_data.ipynb. 
We have tried using metaphor detection algorithms but have not been able to find one that was able to filter any quotes. In the subsequent project process, we will explore better filtering methods.

We also need to accurately identify what triggers discussion around climate change. No current database tracks for example climate change conferences that spark discussion but we will have to take them into account. This problem can be dealt with by filtering out certain known events and by focusing on periods when major natural disasters have occured using the EM-DAT database.

To process and examine the data, we have counted the occurences of the keywords and then performed a rolling average to smooth our data. Then, a simple cross correlation function shows significant correlation. 

In order to analyze public sentiment towards climate change and natural disasters, we give each quote a positive/negative score and subjective/objective score. 
This not only helps us analyze public sentiment changes and correlations, but also helps us filter out some irrelevant data. Test code of this part is in the sentiment-analysis folder, and we will integrate it into the process notebook during the subsequent project process.

Using EM-DAT database to classify natural disasters in terms of severity and region, and the number of discussions resulting from different regions and different levels of natural disaster severity were analysed separately and compared.

## **Proposed Timeline**

- Week 1 (next week): Initial data analysis
- Week 2: In-depth analysis (effects of different indicators etc..)
- Week 3: More analysis and maybe some regression (estimate effect of hypothetical disasters)
- Week 4: Add everything together
- Week 5 (submission week): Final Touches

## **Internal Milestones**

- Peng
    - Area correlation analysis, Hypothetical experiments and analysis.
    - Analyse the impact of climate change on public sentiment，and the degree of impact of different natural disasters on public sentiment，find the correlations.
- Colin
    - Creating the pertinent plots and visualizations for the website.
    - Language analysis and detection of metaphors for pre-processing.
- Gil
    - Evaluate if certain disasters cause more discussion
    - Create skeleton of website

## **Structure of Notebooks**

The code is organised notebooks related to each step of the data analysis :

### **extract_data.ipynb**

Extract data from the json files. <br> 
This notebook will search for any quotes from a list of speakers containing any of the keywords in a list of keywords and write a binary pickle file containing the data.

### **filter_data.ipynb**

Filtering of false positives for certain keywords that are subject to metaphorical uses. 

### **emdat.ipynb**

Loading and cleaning of the dataset taken from the EM-DAT database.

### **process.ipynb**

Process data from both the Quotebank dataset as well as the EM-DAT dataset. Plot evolutions of discussion around topics and of the impacts of natural disasters.

### **sentiment_test.py**
Based on third party github repositories 'TextBlob' ,giving sentiment scores for quotes. (*in progress*)

***The json files should be stored in the data folder to execute the code.***

## **Conclusion**

We believe our initial tinkering shows that the problem we wish to tackle exists and our questions have meaningful answers to be found, and we feel confident that the subject we wish to explore could lead to interesting and insightful data.

# Milestone 3

## **Structure of Notebooks And Files**

All notebooks and scripts (defining helper functions and constants) are under ``code``.

### **emdat.ipynb**

From Milestone 2: renamed to clean_emdat.ipynb

### **disaster_extr_helpers.py**

Defines a set of helper functions mainly for extraction of quotes from Quotebank and performing computations related to extraction.

### **disaster_and_climate_extraction.py**

Extracts a subset of the Quotebank dataset which matches regex patterns (defined in ``disaster_extr_constants.py``) for general storms, heat waves and climate change. It performs this task for each year and saves the compressed data frames to disk.

### **general_token_extraction.py**

Extracts a subset of the Quotebank dataset which matches the token 'especially'. It performs this task for each year and saves the compressed data frames to disk.

### **disaster_extr_constants.py**

Constants (mainly tags for regex patterns and disaster configurations) used for data extraction. Large parts not used in final analyses. Only climate_tags_pos, storm_tags_general and heat_tags_general used in ``disaster_and_climate_extraction.py``.


# Contribution

**Colin**: TODO.

**Gil**: Worked on extracting the quotes pertaining to heat waves and storms throughout 2015-2020 from Quotebank. Quotes from specific disasters were extracted but ultimately not used. Worked on developing the plots for the 'relevant spikes' as well as their analyses.

**Peng**: TODO.



