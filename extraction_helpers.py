import pandas as pd
import bz2
import json

def extract_quotes_speaker(chunk, speaker):
    ### Helper function to extract all quotes from a given speaker

    print(f'Processing chunk with {len(chunk)} rows, looking for quotes from {speaker}.')
    return chunk[chunk['speaker'] == speaker]

def extract_quotes_keyword(chunk, keyword):
    ### Helper function to extract all quotes containing a specific keyword (case-sensitive)

    print(f"Processing chunk with {len(chunk)} rows, looking for quotes containing '{keyword}'.")
    return chunk[chunk["quotation"].str.contains(keyword, na=False)]

def extract_quotes_speaker_keyword(chunk, speaker, keyword):
    ### Helper function to extract all quotes containing from a given speaker containing a specific keyword (case-sensitive)

    print(f"Processing chunk with {len(chunk)} rows, looking for quotes from {speaker} containing '{keyword}'.")
    return chunk.loc[(chunk["quotation"].str.contains(keyword, na=False)) & (chunk["speaker"] == speaker)]

def extract_quotes(data, speaker = False, keyword = False,  chunksize = 1000000, compression = 'bz2'):
    ### Extract all quotes containing from a given speaker containing a specific keyword (case-sensitive)

    # initialize a Dataframe
    df = pd.DataFrame({'quoteID':'', 'quotation':'', 'speaker':'', 'qids':'', 'date':'', 'probas':'', 'numOccurences':'', 'phase':''}, index = [0])

    # Trying to extract the whole dataset
    if not speaker and not keyword:
        print("You're attempting to extract the whole dataset, please select a speaker and/or a keyword.")
    

    else:
        with pd.read_json(data, lines=True, compression=compression, chunksize=chunksize) as df_reader:
            
            # Speaker and keyword are given :
            if speaker and keyword:
                for chunk in df_reader:
                    quotes = extract_quotes_speaker_keyword(chunk, speaker, keyword)
                    df = pd.concat([df, quotes], ignore_index=True)
                

            # Speaker is given
            elif speaker:
                for chunk in df_reader:
                    quotes = extract_quotes_speaker(chunk, speaker)
                    df = pd.concat([df, quotes], ignore_index=True)
                

            # Keyword is given
            else:
                for chunk in df_reader:
                    quotes = extract_quotes_keyword(chunk, keyword)
                    df = pd.concat([df, quotes], ignore_index=True)
            
            return df.iloc[1: , :]
                
    