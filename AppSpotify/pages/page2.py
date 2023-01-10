import streamlit as st
import pandas as pd
import plotly.graph_objs as go

st.title("Something with artists")

df = pd.read_json('..\Lukasz\long\endsong_0.json')
all_artists = len(df)

artists_count = df.master_metadata_album_artist_name.value_counts().head(10)
artists_count = pd.Series.to_frame(artists_count).rename_axis("artist").reset_index().rename(
    columns={"master_metadata_album_artist_name": "count"})

df = pd.DataFrame({'artist': ['all_artists'], "count": [all_artists]})
df = df.append(artists_count, ignore_index=True)

label = df['artist']
source = [0] * (len(df['artist']) - 1)
target = [_ for _ in range(1, (len(df['artist'])))]
value = df['count'].iloc[1:(len(df['artist']))].tolist()
print(source)
print(target)
print(value)
fig = go.Figure(data=[go.Sankey(
    node=dict(
        label=df['artist'],
    ),
    link=dict(
        source=source,
        target=target,
        value=value
    )
)])

fig.update_layout(title_text="Top 10 artystów dla Łukasza", font_size=10)

st.pyplot(fig)