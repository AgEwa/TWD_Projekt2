import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('C:/Users/karim/PycharmProjects/TWD_Projekt2/AppSpotify/karolina.csv', index_col = 0)
df['secPlayed'] = df['msPlayed'] / 1000
df = df[df.columns[:-1].insert(4, df.columns[-1])]
df = df[df.secPlayed > 60]
features = ['danceability', 'energy', 'speechiness', 'instrumentalness', 'valence']


st.title("What music do we listen to?")
# # st.sidebar.success("Select page above.")
#
st.write("Check who are the artist we most frequently listen to. Maybe you know a few?")
st.write("What are the song's features we long for the most?\n"
         "Is valence more important then energy or maybe we want to listen to danceable songs?\n"
         "Find out!")
hours = st.slider('Choose time range', 0, 24, (8,16))

df['datetime']=pd.to_datetime(df['datetime']).dt.hour
df1=df[(df.datetime<=hours[1]) & (df.datetime>=hours[0])]
for feature in features:
    df1[f'{feature}_mean'] = df1[feature].mean()

df1=df1.reset_index(drop = True)
df2=df1.groupby("artistName").size().reset_index().rename(columns={0: 'Count'}).sort_values("Count", ascending=False).reset_index(drop = True).head(3)


fig = px.line_polar(r=df1.loc[0,["danceability_mean","energy_mean","speechiness_mean","instrumentalness_mean","valence_mean"]], theta=features, line_close=True,template="plotly_dark")
fig.update_traces(fill='toself')
fig.update_polars(radialaxis_range=[0,1])

fig = px.line_polar(r=df1.loc[0,["danceability_mean","energy_mean","speechiness_mean","instrumentalness_mean","valence_mean"]], theta=features, line_close=True)

# wstawić kolor
fig.update_layout(polar_bgcolor= 'white')
fig.update_traces(fill='toself')
fig.update_polars(radialaxis_range=[0,1])

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.title('First incredible anonymous person ')
        st.write("Top artists")
        st.table(df2["artistName"])
    with col2:
        st.plotly_chart(fig, height=100)
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.title('Second incredible anonymous person ')
        st.write("Top artists")
        st.table(df2["artistName"])
    with col2:
        st.plotly_chart(fig,height=100)
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.title('Third incredible anonymous person ')
        st.write("Top artists")
        st.table(df2["artistName"])

    with col2:
        st.plotly_chart(fig,height=100)