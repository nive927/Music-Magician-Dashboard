import streamlit as st
import pandas as pd
import plotly.express as px

# Load Data
df = pd.read_csv('Data/data_by_year.csv')
df_full = pd.read_csv('Data/full_music_data.csv')

# Calculate % songs containing explicitness music by year using full dataset
df['explicitness'] = df_full.groupby(['year'])['explicit'].mean().reset_index().explicit

# Title
st.title('Data by Year')

st.write(
    """
The visualizations on this page aim to examine how cultural changes and 
advancements in music technology are reflected in music characteristics and 
vice versa. The values in this dataset were found by aggregating the values for
each song in a given year in the full dataset in an attempt to represent the
"average" values for that year.
\n
The data for each visualization can be found in the "Data" of the respective graph.
    """
)

st.divider()

st.header("The Rise of Electronic Music")
tab1, tab2 = st.tabs(["Plot", "Data"])
with tab1:
    fig = px.line(df, x="year", y=["energy", "acousticness", "instrumentalness"],
                title="Energy, Acousticness, and Instrumentalness Over Time")
    fig.update_layout(xaxis_title='Year', yaxis_title='Value')
    st.plotly_chart(fig, use_container_width=True)
with tab2:
    st.dataframe(df[['year', 'energy', 'acousticness', 'instrumentalness']])

st.write(
    """
Starting in the 1950s with the introduction of electronic augmentation, we can 
visually discern how quickly it takes over. Acousticness and instrumentalness
in music experienced a stark decline starting in the 1950s and leveling off
around 1980, while energy saw a steady increase over the same time period. Since
then, all three characteristics have remained relatively stable.
\n
The 1950s saw the invention of synthesizers, which in simplified
terms is are machines that generate audio signals via electronic means. Prior to
the onset of the synthesizer, new electronic instruments like the electric 
guitar, electric bass, and electric keyboard had begun to emerge and rapidly
gain popularity.
\n
The 1970s experienced a boom in electronic music as synthesizers became more
portable and widely available. It was these improvements that standardized the
concept of synthesizers as self-contained instruments with built-in keyboards.
    """
)

st.divider()

st.header("Faster, Louder, More Explicit")
tab1, tab2 = st.tabs(["Plot", "Data"])
with tab1:
    fig = px.area(df, x="year", y="loudness",
                title="Average Loudness of Songs Over Time")
    fig.update_layout(xaxis_title='Year', yaxis_title='Decibels')
    st.plotly_chart(fig, use_container_width=True)
with tab2:
    st.dataframe(df[['year', 'loudness']])

st.write(
    """
The values in this feature may be difficult to interpret, but in the context of
audio and decibels, a negative value doesn't represent a negative loudness! The 
decibel (dB) scale is logarithmic and is often used in audio to express the
relative intensity or power of a sound compared to some reference level.
Although the official documentation of this dataset does not specify what the
specific reference level is, we are still able to observe that over time, the 
average loudness of songs has become less negative, meaning that songs have 
become louder and louder.
    """
)

tab1, tab2 = st.tabs(["Plot", "Data"])
with tab1:
    fig = px.line(df, x="year", y="tempo",
                title="Tempo of Songs Over Time")
    fig.update_layout(xaxis_title='Year', yaxis_title='Beats per Minute')
    st.plotly_chart(fig, use_container_width=True)
with tab2:
    st.dataframe(df[['year', 'tempo']])

st.write(
    """
Interestingly, we also see a strong change in the average tempo of songs between
1950 and 1980 similar to the trend observed in the characteristics mentioned in 
the previous section. In general, this three decade period saw multiple 
characteristics of music undergo rapid changes which have not reverted to pre-1950
states.
    """
)

tab1, tab2 = st.tabs(["Plot", "Data"])
with tab1:
    fig = px.area(df, x="year", y="explicitness",
                title="Proportion of Songs Containing Explicitness Over Time")
    fig.update_layout(xaxis_title='Year', yaxis_title='Proportion of Songs')
    st.plotly_chart(fig, use_container_width=True)
with tab2:
    st.dataframe(df[['year', 'explicitness']])

st.write(
    """
In recent years, almost a quarter of music on Spotify contains some degree of
explicitness; prior to 1980, this proportion was less than 1%. These values may
potentially be slightly smaller than true values, as in this parrticular dataset,
a value of 0 for explicitness could also mean that the explicitness of the song
is unknown.
\n
The rise of explicitness in music is likely due to a combination of factors,
one of which could be Western culture's increasing acceptance of more graphic
topic which have become more prevalent in music over time. However, from listening
to older music, many users can likely observe that older music defers more towards
euphemisms than outright explicitness; we postulate then that cultural liberalism
plays a significant role in the stark increase in explicitness in music that we 
see in this data in addition to strong shifts in topics in music, which is still
likely the largest factor in this change.  
    """
)

st.divider()

st.header("G and A# Rule All Other Keys")
col1, col2 = st.columns(2)

with col1:
    st.write(
    """
    In this dataset, keys for each year are calculated as the estimated overall key 
    of each track, and then taking the dominant key of each year as the key with the
    most occurrences in that year. This is not a perfect method, as it does not
    account for the key changes within songs, but it serves as a decent 
    approximation of the key distribution of songs over time.
    \n
    Using standard pitch class notation where pitches are mapped to an integer, 
    we can see that the dominant keys are 7 and 10, which correspond to G and A#,
    respectively.
    \n
    There are many hypotheses as to why these keys like G-Major have been so
    popular throughout history. One theory is that major keys are typically
    perceived as happier, while another theory is that keys like G-Major and
    C-Major are convenient to play on both the piano and the guitar, two 
    instruments that dominate Western contemporary music (the largest
    composition of this dataset).
    """
    )

with col2:
    tab1, tab2 = st.tabs(["Plot", "Data"])
    temp = df.key.value_counts()
    with tab1:
        fig = px.pie(temp, values=df.key.value_counts(), names=df.key.unique(),
                    title='Average Key Distribution of Songs, 1921-2020')
        fig.update_layout(legend_title_text='Key')
        st.plotly_chart(fig, use_container_width=True)
    with tab2:
        st.dataframe(temp)

st.divider()

st.header("Evolution of Music Characteristics Over Time")
st.write(
    """
The customizable graph below allows the exploration of how the selected music
characteristics have changed over time. We encourage users to select different
time ranges and characteristics to observe trends in more or less detail.
\n
The data plotted in the graph is included in the "Data" tab below.
    """
)

start_year, end_year = st.select_slider(
    'Select a range of years to visualize',
    options = df.year.unique(),
    value=(max(df.year.unique()), min(df.year.unique())))

characteristics = st.multiselect(
    'Select characteristics to visualize',
    ['danceability', 'energy', 'valence', 'acousticness', 'instrumentalness',
     'explicitness', 'liveness', 'speechiness'],
    ['valence', 'acousticness', 'liveness'])

df_filtered = df[['year'] + characteristics]
df_filtered = df_filtered[(df_filtered['year'] >= start_year) & 
                          (df_filtered['year'] <= end_year)]

tab1, tab2 = st.tabs(["Plot", "Data"])

with tab1:
    fig = px.line(df_filtered, x="year", y=characteristics,
                  title="Music Characteristics Over Time")
    fig.update_layout(xaxis_title='Year', yaxis_title='Value')
    fig.update_layout(legend_title_text='Characteristic')
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.dataframe(df_filtered)


st.divider()

st.subheader("References")

st.write(
"""
- [Synthesizer, Wikipedia](https://en.wikipedia.org/wiki/Synthesizer)

"""
)


# References

# https://courses.lumenlearning.com/suny-musicapp-medieval-modern/chapter/electronic-music/#:~:text=Music%20produced%20solely%20from%20electronic,the%20purpose%20of%20composing%20music.

# https://www.digitaltrends.com/music/whats-the-most-popular-music-key-spotify/

# https://mixedinkey.com/captain-plugins/wiki/best-chords-for-edm/



