import streamlit as st
import pandas as pd, numpy as np
import plotly.express as px

df = pd.read_csv('karolina.csv', index_col = 0)
df['secPlayed'] = df['msPlayed'] / 1000
df = df[df.columns[:-1].insert(4, df.columns[-1])]
df = df[df.secPlayed > 60]
features = ['danceability', 'energy', 'speechiness', 'instrumentalness', 'valence']
for feature in features:
    df[f'{feature}_mean'] = df[feature].mean()

fig = px.line_polar(r=df.loc[0,["danceability_mean","energy_mean","speechiness_mean","instrumentalness_mean","valence_mean"]], theta=features, line_close=True,template="plotly_dark")
fig.update_traces(fill='toself')
fig.update_polars(radialaxis_range=[0,1])
fig.show()

st.title("What music do we listen to?")
# # st.sidebar.success("Select page above.")
#
st.write("top artists, top sonds, music type (?)")
