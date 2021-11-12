from extraction_helpers import *
import pandas as pd
import bz2
import json
import pickle
import numpy as np
from textblob import TextBlob #An unofficial natural language processing repository

'''extraction quotations form dataset'''
data = 'data/quotes-2019-nytimes.json.bz2'

speakers = False
keywords = ['hurricane']

dict_df = extract_quotes(data, speakers=speakers, keywords= keywords)
hurricane_quotation = dict_df['hurricane']['quotation']
quotation_sentences= hurricane_quotation.values

'''calculate the score of Optimism and Pessimism [-1.0, 1.0], score of subjective and objective[0.0, 1.0], where 0.0 is very objective and 1.0 is very subjective.'''

score_op_pe = []
score_sub_obj = []
for x in quotation_sentences.flat:
    quota = TextBlob(x)
    print(x)
    print('score',quota.sentiment,quota.sentiment.polarity)
    score_op_pe.append(quota.sentiment)
    score_sub_obj.append(quota.sentiment.polarity)

'''we can also use this find Part-of-speech tags, this may useful to metaphor detection'''
#example
example = TextBlob(quotation_sentences[0])
print(example.tags)

