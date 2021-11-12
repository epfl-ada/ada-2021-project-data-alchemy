
### -------- IMPORTS -----------------------------------------------------------------------------------------

import pandas as pd
import bz2
import json


### ------------------ HELPER FUNCTIONS-----------------------------------------------------------------------

def extract_quotes_speaker(chunk, speakers):
    ### Helper function to extract all quotes from a list of speakers (case-sensitive)
    ### Returns a dictionary of dataframes

    # If only one speaker, turn it into a list
    if type(speakers) == str:
        speakers = [speakers]

    # For each speaker, extract the quotes from the chunk
    dict_speakers = {}
    for speaker in speakers: # This would not work if speakers were not a list
        print(f'Processing chunk with {len(chunk)} rows, looking for quotes from {speaker}.')
        dict_speakers[speaker] = chunk[chunk['speaker'] == speaker]
    return dict_speakers


def extract_quotes_keyword(chunk, keywords):
    ### Helper function to extract all quotes containing a list of keywords (case-sensitive)
    ### Returns a dictionary of dataframes

    # If only one keyword, turn it into a list
    if type(keywords) == str:
        keywords = [keywords]
    
    # For each keyword, extract the quotes from the chunk
    dict_keywords = {}
    for keyword in keywords:
        print(f"Processing chunk with {len(chunk)} rows, looking for quotes containing '{keyword}'.")
        dict_keywords[keyword] = chunk[chunk["quotation"].str.contains(keyword, na=False)]
    return dict_keywords


def extract_quotes_speaker_keywords(chunk, speaker, keywords):
    ### Helper function to extract all quotes from **a given speaker** containing a list of keywords (case-sensitive)
    ### Returns a dictionary of dataframes

    # If only one keyword, turn it into a list
    if type(keywords) == str:
        keywords = [keywords]
    
    # For each keyword, extract the quotes from the given speaker from the chunk
    dict_speaker_keywords = {}
    for keyword in keywords:
        print(f"Processing chunk with {len(chunk)} rows, looking for quotes from {speaker} containing '{keyword}'.")
        dict_speaker_keywords[keyword] = chunk.loc[(chunk["quotation"].str.contains(keyword, na=False)) & (chunk["speaker"] == speaker)]
    return dict_speaker_keywords


### ----------------------- EXTRACTION FUNCTION ---------------------------------------------------------------------------------------

def extract_quotes(data, speakers = False, keywords = False,  chunksize = 1000000, compression = 'bz2'):
    ### Extract all quotes from a list of speakers containing a list of keywords (keyword 1 OR keyword 2 OR ...) (case-sensitive)

    # Trying to extract the whole dataset
    if not speakers and not keywords:
        print("You're attempting to extract the whole dataset, please select (a) speaker(s) and/or (a) keyword(s). \n\
            For multiple speakers or keywords, use a list.")
    

    else:
        with pd.read_json(data, lines=True, compression=compression, chunksize=chunksize) as df_reader:
            
            # Speaker and keyword are given :
            if speakers and keywords:
                if type(speakers) == str:
                    speakers = [speakers]
                if type(keywords) == str:
                    keywords = [keywords]

                dict_speakers_keywords = {}

                
                for speaker in speakers:
                    dict_speakers_keywords[speaker] = {}
                    for keyword in keywords:
                        dict_speakers_keywords[speaker][keyword] = pd.DataFrame({'quoteID':'', 'quotation':'', 'speaker':'',\
                        'qids':'', 'date':'', 'probas':'', 'numOccurences':'', 'phase':''}, index = [0])
                
                for chunk in df_reader:
                    for speaker in speakers:
                        quotes = extract_quotes_speaker_keywords(chunk, speaker, keywords)
                        for keyword in keywords:
                            dict_speakers_keywords[speaker][keyword] = pd.concat([dict_speakers_keywords[speaker][keyword], quotes[keyword]], ignore_index=True)
                
                for speaker in speakers:
                    for keyword in keywords:
                        dict_speakers_keywords[speaker][keyword] = dict_speakers_keywords[speaker][keyword].iloc[1:, :]
                
                return dict_speakers_keywords


                

            # Speaker is given
            elif speakers:
                if type(speakers) == str:
                    speakers = [speakers]
                dict_speakers = {}
                for speaker in speakers:
                    dict_speakers[speaker] = pd.DataFrame({'quoteID':'', 'quotation':'', 'speaker':'',\
                         'qids':'', 'date':'', 'probas':'', 'numOccurences':'', 'phase':''}, index = [0])

                for chunk in df_reader:
                    quotes = extract_quotes_speaker(chunk, speakers)
                    for speaker in speakers:
                        dict_speakers[speaker] = pd.concat([dict_speakers[speaker], quotes[speaker]], ignore_index=True)
                
                for speaker in speakers:
                    dict_speakers[speaker] = dict_speakers[speaker].iloc[1:, :]
                
                return dict_speakers
                

            # Keyword is given
            else:
                if type(keywords) == str:
                    keywords = [keywords]
                dict_keywords = {}
                for keyword in keywords:
                    dict_keywords[keyword] = pd.DataFrame({'quoteID':'', 'quotation':'', 'speaker':'',\
                         'qids':'', 'date':'', 'probas':'', 'numOccurences':'', 'phase':''}, index = [0])

                for chunk in df_reader:
                    quotes = extract_quotes_keyword(chunk, keywords)
                    for keyword in keywords:
                        dict_keywords[keyword] = pd.concat([dict_keywords[keyword], quotes[keyword]], ignore_index=True)
                
                for keyword in keywords:
                    dict_keywords[keyword] = dict_keywords[keyword].iloc[1:, :]
            
                return dict_keywords
