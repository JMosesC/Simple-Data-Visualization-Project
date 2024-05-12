import os
import pandas as pd
import streamlit as st

def clean_df(df):
    """
    From a Dataframe, drop:
        1. Empty rows
        2. Products not supported on any system (Non-game products)
    Dataset has no duplicate entries.
    """
    df = df.dropna()
    filtered_df = df.query("win or mac or linux")
    
    return filtered_df

def get_metadata():
    path = os.path.join('data', 'games_metadata.json')
    metadata = pd.read_json(path, lines=True)
    metadata = metadata.drop(columns=['description'])
    
    return metadata

@st.cache_data
def get_data():
    """
    Retrieves data from the source files, and cleans it.
    """
    path = os.path.join('data', 'data.csv')
    data = pd.read_csv(path)
    metadata = get_metadata()
    df = pd.merge(data, metadata)
    df = clean_df(df)
    
    return df

@st.cache_data
def filter_tag(df, tags):
    """
    From the dataset, retrieve only rows where all product tags listed
    in the 'tags' argument can be found in an individual product's list of tags.
    """
    if not tags:
        filtered = df
    else:
        filtered = df[df['tags'].apply(lambda x: all(item in x for item in tags))]
        
    return filtered

@st.cache_data
def bin_df(df, bins, labels):
    """
    Converts continuous data into categorical data by assigning
    values to bins, depending on which range of values they belong to.
    """
    binned = pd.cut(df, bins=bins, labels=labels)
    return binned

@st.cache_data
def get_tags(df):
    """
    Retrives list of all unique tags from all products in the dataset.
    """
    tags = list(df['tags'].explode().unique())
    return tags