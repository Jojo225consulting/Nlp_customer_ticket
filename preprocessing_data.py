import polars as pl
import pandas as pd
import numpy as np

def make_clean(data_path, feature_target=['body','queue','language']):
    ''' This function allows to make clean data'''
    df=pl.read_csv(data_path)

    #dropping columns containing totaly Null value
    df_clean = df.select([col for col in df.columns if df.select(col).null_count().item() < len(df)])

    #dropping rows containing totaly Null value
    df_clean = df_clean.filter(~pl.all_horizontal(pl.col('*').is_null()))
    
    #dropping every row containing Null value in one of element from list feature_target
    for col in feature_target:
        df_clean = df_clean.filter(pl.col(col).is_not_null())
    
    if df_clean.shape == df.shape: 
        print("No difference between after cleaning")
    else:
        print("Some elements have been dropped during cleaning")
    
    return df_clean



def synonym_verif(word, corpus):
    '''This function consists to verify if a word coming from a new request already exists in the corpus. 
    If not the case, we attempt to replace this word by the nearest word present in the corpus provided that the threshold of similarity be more than 0.65'''
    # import fasttext

    # model = fasttext.load_model('/kaggle/input/fasttext-cc-en-300-bin/cc.en.300.bin')

    nearest = word
    if word not in corpus:
        similar_words = model_synonym.get_nearest_neighbors(word, k=10)
        for similarity, w in similar_words :
            if (w in corpus) and (similarity >= 0.7):
                nearest = w
                break

    return nearest



def clean_sentence(sentence, corpus):
    """
    Applique synonym_verif à chaque mot d'une phrase.
    """
    words = sentence.split()
    corrected_words = [synonym_verif(word, corpus) if word not in text.ENGLISH_STOP_WORDS else word for word in words]
    return " ".join(corrected_words)