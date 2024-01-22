import streamlit as st
import pandas as pd
import numpy as np
import datetime

import altair as alt
import matplotlib.pyplot as plt

import plotly.express as px
import plotly.graph_objects as go


df = pd.read_csv('data/full_music_filtered_by_date.csv')
df['release_date'] = pd.to_datetime(df['release_date'])

st.title("Data by Song")

st.markdown("This interactive page allows you to explore characteristics of different songs. You can navigate to the overview tabs to view the full music distribution, the song ranking tab to see top or least favored songs in different time range, and the comparison tab to compare characteristics of different songs")

df.iloc[:, 2:14] = df.iloc[:, 2:14].astype('float')

# Numeric columns only
subset = df[df.columns[2:-2]]


# Create three tabs
tab1, tab2, tab3 = st.tabs(['Overview', 'Song Ranking', 'Song Comparison'])


# Show overview graphs
with tab1:
    st.header("Dataset distribution")
    st.markdown("""
        This tab is a static tab that shows statistics of the original dataset,
        including the correlation matrix of the numeric features in the
        dataset, the entire original dataset, and statistics of numerical
        features such as min, max, and standard deviation.
        """)

    st.subheader("Correlation matrix of numerical features")
    st.markdown("""
        Here is the correlation matrix of the numerical features of the entire
        dataset. Interestingly, there actually isn't too much interesting
        correlations between features except for those who are inherently
        correlated (e.g. energy songs are usually loud, but also low in
            acousticness). One interesting fact is that popularity seem to be
        correlated with year, but this is highly likely to be a case of
        correlation without causation
    """)

    f = plt.figure(figsize=(15,15))
    plt.matshow(subset.corr(), fignum=f.number)
    plt.xticks(range(subset.select_dtypes(['number']).shape[1]), subset.select_dtypes(['number']).columns, fontsize=14, rotation=45)
    plt.yticks(range(subset.select_dtypes(['number']).shape[1]), subset.select_dtypes(['number']).columns, fontsize=14)
    cb = plt.colorbar()
    cb.ax.tick_params(labelsize=14)

    st.pyplot(f)


    st.subheader("Originl Dataset")
    st.dataframe(df)

    st.subheader("Statistics of numerical features")
    st.dataframe(df.describe())



# Show song rankings
with tab2:
    st.header("Top & bottom k songs")
    st.markdown("""
        Use the interactive widgets in this tab to filter the original dataset to view the most and least popular songs. You can also hover over the graph to see specific popularity score of the song!
    """)
    col1, col2 = st.columns(2)
    with col1:
        # filter by date
        date_range = st.slider(
                "Time Range",
                df['release_date'].min(), 
                df['release_date'].max(),
                (
                    df['release_date'].min().to_pydatetime(), df['release_date'].max().to_pydatetime()
                    )
                )


    with col2:
        # filter by top/bottom k
        k = st.number_input(
                "Choose k",
                1, 50, 10
                )

    rank_subset = df[df['release_date'] >= date_range[0]]
    rank_subset = rank_subset[rank_subset['release_date'] <= date_range[1]]
    rank_subset = rank_subset[rank_subset['popularity'] != 0]

    # cap max popularity
    cap_pop = st.slider("Minumum/Maximum popularity of shown songs",
                int(rank_subset['popularity'].min()),
                int(rank_subset['popularity'].max()),
                (int(rank_subset['popularity'].min()), int(rank_subset['popularity'].max()))
            )


    rank_subset = rank_subset[rank_subset["popularity"] <= cap_pop[1]]
    rank_subset = rank_subset[rank_subset["popularity"] >= cap_pop[0]]

    rank_subset = rank_subset.sort_values(by='popularity' )

    fig1 = alt.Chart(
            rank_subset.tail(k)[::-1],
            title=f"Top {k} most popular songs"
        ).mark_bar().encode(
            alt.X("popularity:Q"),
            alt.Y("song_title (censored):N", sort=("-x")),
            fill=alt.Color("popularity:Q", scale=alt.Scale(scheme="greenblue")),
            tooltip=["song_title (censored)", "artist_names", "popularity", "year"]
        ).transform_window(
            rank="rank(popularity)",
            sort=[alt.SortField("popularity", order="ascending")]
        ).transform_filter(
            (alt.datum.rank <= k)
        )
    st.altair_chart(fig1, use_container_width=True)

    fig2 = alt.Chart(
            rank_subset.head(k)[::-1],
            title=f"Bottom {k} least popular songs"
        ).mark_bar().encode(
            alt.X("popularity:Q"),
            alt.Y("song_title (censored):N", sort=("x")),
            fill=alt.Color("popularity:Q", scale=alt.Scale(scheme="darkred")),
            tooltip=["song_title (censored)", "artist_names", "popularity", "year"]
        ).transform_window(
            rank="rank(popularity)",
            sort=[alt.SortField("popularity", order="ascending")]
        ).transform_filter(
            (alt.datum.rank <= k)
        )
    st.altair_chart(fig2, use_container_width=True)




# Compare songs
df['song_artist'] = df['song_title (censored)'] + " by " + df['artist_names']

with tab3:
    st.header("Song Comparison")
    st.markdown("""
        In this tab, you can freely select up to 6 songs present in the original dataset to view and compare the different features of the songs. You can also interact with the graph such as zoom in and hide multiple songs to make comparison easier!
    """)

    songs = st.multiselect("Select up to 6 songs to compare", df['song_artist'].sort_values(),
            placeholder="Choose songs", 
            max_selections = 6,
            default = ["Stuck with U (with Justin Bieber) by ['Ariana Grande', 'Justin Bieber']",
                "I Know You Care by ['Ellie Goulding']"]) 

    comp_subset = df[ df['song_artist'].isin(songs) ]

    cols = ["danceability", "energy", "valence", "acousticness", "instrumentalness", "liveness", "speechiness"]

    plot_data = list()
    for song in songs:
        song_row = comp_subset[comp_subset['song_artist'] == song].squeeze()

        plot_data.append(go.Scatterpolar(r=song_row[cols].to_list(), theta=cols, fill="toself", name=song_row["song_artist"], text=f"Popularity: {str(song_row['popularity'])}"))

    fig = go.Figure(
        data=plot_data,
        layout=go.Layout(
            title=go.layout.Title(text=""),
            polar={"radialaxis": {"visible": True}},
            showlegend=True
        )
    )

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.2,
        xanchor="right",
        x=1
    ))

    st.markdown('')
    st.markdown('')

    st.plotly_chart(fig)


