import numpy as np
import pandas as pd
import streamlit as st
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go
from utils import get_data, bin_df, get_tags, filter_tag

df = get_data()
tags = get_tags(df)
st.header("Steam Game Statistics")

# Tabs layout
tab1, tab2, tab3 = st.tabs(["Descriptive Statistics", "Inferential Statistics", "Raw Data"])

# Descriptive statistics tab
with tab1:
    vert_space = '<div style="padding: 30px 5px;"></div>'
    st.markdown(vert_space, unsafe_allow_html=True)
    
    # Filter data via tags
    options = st.multiselect(
        "Optional: Include only products with the following tags: ",
        options=tags, default=None, 
    )
    df_tab1 = filter_tag(df, options)
    
    # Display count of unique games
    st.write("### Number of games: ", df_tab1['title'].nunique())
    
    # Plot system compatibility
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Mac", "Linux"),
        specs=[[{"type": "pie"}, {"type": "pie"}]])
    
    # Mac compatibility
    fig.add_trace(
        go.Pie(
            values=df_tab1['app_id'], 
            labels=df_tab1['mac']),
        row=1, col=1)
    
    # Linux compatibility   
    fig.add_trace(
        go.Pie(
            values=df_tab1['app_id'], 
            labels=df_tab1['linux']),
        row=1, col=2)
    
    fig.update_layout(title_text="Non-Windows System Compatibility")
    st.plotly_chart(fig)

    # Plot distribution of overall ratings
    fig = px.pie(
        df_tab1, names='rating',
        title="Distribution of Overall Game Ratings")
    st.plotly_chart(fig)

    # Graph positive rating ratios
    ratios = bin_df(df_tab1['positive_ratio'], 
                bins=[0, 20, 40, 60, 80, 100], 
                labels=['0-20', '20-40', '40-60', '60-80', '80-100'])
    fig = px.bar(ratios, title="Positive Rating Ratios Per Game")
    st.plotly_chart(fig)
    
    # Graph game prices
    prices = bin_df(df_tab1['price_final'], 
                bins=[0, 15, 30, 45, 60, np.inf], 
                labels=['Below $15', '$15-30', '$30-45', '$45-60', 'Above $60'])
    fig = px.bar(prices, title="Game Prices")
    fig.update_layout(xaxis={'categoryorder':'array', 
                             'categoryarray':['Below $15', '$15-30', '$30-45', '$45-60', 'Above $60']})
    st.plotly_chart(fig)


# Inferential statistics tab
with tab2:
    vert_space = '<div style="padding: 30px 5px;"></div>'
    st.markdown(vert_space, unsafe_allow_html=True)
    
    # Heatmap between positive rating ratios and game price
    max_price = int(df['price_final'].max())
    price_value = st.number_input(
        f"Limit of range of price values (max: ${max_price}):",
        min_value=1, max_value=max_price, value=60,
    )
    sliced = df[df['price_final'] <= price_value]
    fig = px.density_heatmap(
        sliced, x='positive_ratio', y='price_final',
        title="Positive Rating Ratios for Games by Game Prices"
    )
    st.plotly_chart(fig)
    
    # Graph between positive rating ratios and number of reviews
    max_revs = int(df['user_reviews'].max())
    revs_value = st.number_input(
        f"Limit of range of review counts (max: {max_revs}):",
        min_value=1, max_value=max_revs, value=200000,
    )
    sliced = df[df['user_reviews'] <= revs_value]
    fig = px.scatter(
        sliced, x='positive_ratio', y='user_reviews',
        title="Positive Rating Ratios for Games by Number of Reviews",
        
    )
    st.plotly_chart(fig)

with tab3:
    st.subheader("Raw Data")
    st.dataframe(df)