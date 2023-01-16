import streamlit as st
import pandas as pd
import plotly.graph_objs as go

st.title("Something with artists")

df1 = pd.read_json('./Lukasz/long/endsong_0.json')
df2 = pd.read_json('./Agata/extended/endsong_0.json')

artist_chosen = 'The Dumplings'

names = ["Łukasz", "Agata", "Karolina"]
frames = [df1, df2]
df_plot_year = None
df_plot_name = None
all_of_artist = 0
year_len = []
i = 0
for df in frames:
    # Filtering for chosen artis by year
    df_filter_by_artist = df.loc[
        df.master_metadata_album_artist_name == artist_chosen].reset_index(drop=True)
    df_filter_by_artist['Year'] = pd.to_datetime(df_filter_by_artist["ts"]).dt.strftime('%Y')
    df_filter_by_artist = df_filter_by_artist.groupby("Year").master_metadata_album_artist_name.agg(
        'count').reset_index() \
        .rename(columns={"master_metadata_album_artist_name": "count"})
    df_plot_year = pd.concat([df_plot_year, df_filter_by_artist])

    # Summing tracks
    suma = sum(df_filter_by_artist['count'])
    all_of_artist += suma

    # Prepering df with names
    df_plot_name = pd.concat([df_plot_name, pd.DataFrame({
        'Name': [names[i]],
        'count': [suma]
    })])
    i += 1

    year_len.append(len(df_filter_by_artist))

# Data for Sankey diagram
label = ['Sum of all tracks'] + df_plot_name['Name'].tolist() + df_plot_year['Year'].tolist()
source = []
target = []
value = []
for i in range(len(df_plot_name)):
    source += [0]
    target += [i + 1]
value += df_plot_name['count'].tolist()
before = 0
for i in range(len(df_plot_name)):
    for j in range(year_len[i]):
        source += [1 + i]
        target += [1 + len(df_plot_name) + j + before]
    before += year_len[i]
value += df_plot_year['count'].tolist()

# node_x = [0]+[1]*len(df_plot_name)+[2]*len(df_plot_year)
# node_y = [0]+[_ for _ in range(len(df_plot_name))]+[_ for _ in range(len(df_plot_year))]
#
# print(node_x)
# print(node_y)

fig = go.Figure(data=[go.Sankey(
    node=dict(
        label=label
        # x = node_x,
        # y = node_y
    ),
    link=dict(
        source=source,
        target=target,
        value=value
    )
)])

fig.update_layout(title_text=" Sankey plot for chosen artist ", font_size=18)

st.plotly_chart(fig)