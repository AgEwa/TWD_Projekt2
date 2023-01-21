import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

st.title("How much do we share listening to our favourite artists?")

df1 = pd.read_json('./Lukasz/long/endsong_0.json')
df2 = pd.read_json('./Agata/extended/endsong_0.json')
df3 = pd.read_json('./Karolina/endsong.json')


# Searching for top artist for everybody
frames = [df1,df2,df3]
artists_to_choose = []
for df in frames:
    temp = df.master_metadata_album_artist_name.value_counts().head(10).reset_index()
    artists_to_choose += temp["index"].tolist()
artist_chosen = st.selectbox("Choose an artist",
                             artists_to_choose)


# Choosing data frames to use
frames = [] # [df1,df2,df3]
names = [] #["Łukasz", "Agata", "Karolina"]
colors = [] #["#1db954", "#083318", "#10642d"]
node_colors = ["white"]
st.write("Who do you want to compare?")
lukasz = st.checkbox("Łukasz")
if lukasz:
    frames += [df1]
    names += ["Łukasz"]
    colors += ["#1db954"]
    node_colors += ["#179443"]
agata = st.checkbox("Agata")
if agata:
    frames += [df2]
    names += ["Agata"]
    colors += ["#083318"]
    node_colors += ["#062913"]
karolina = st.checkbox("Karolina")
if karolina:
    frames += [df3]
    names += ["Karolina"]
    colors += ["#10642d"]
    node_colors += ["#0d5024"]

if frames:
    df_plot_year = None
    df_plot_name = None
    all_of_artist = 0
    year_len = []
    i = 0
    for df in frames:
        # Filtering for chosen artist by year
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

    if not df_plot_year.empty:
        df_plot_year = df_plot_year.reset_index(drop=True)
        min_year = int(df_plot_year['Year'].min())
        max_year = int(df_plot_year['Year'].max())
        years = list(range(min_year, max_year+1))

        # Data for Sankey diagram
        label = ['Sum of all tracks'] + df_plot_name['Name'].tolist() + years
        source = []
        target = []
        value = []
        color = []
        for i in range(len(df_plot_name)):
            source += [0]
            target += [i + 1]
            color += [colors[i]]
        value += df_plot_name['count'].tolist()

        chosen_year = 0
        for i in range(len(df_plot_name)):
            for j in range(year_len[i]):
                source += [1 + i]
                target += [label.index(int(df_plot_year.loc[chosen_year+j,'Year']))]
                color += [colors[i]]
            chosen_year += year_len[i]
        value += df_plot_year['count'].tolist()

        # node_x = [0]+[1]*len(df_plot_name)+[2]*len(df_plot_year)
        # node_y = [0]+[_ for _ in range(len(df_plot_name))]+[_ for _ in range(len(df_plot_year))]
        #
        # print(node_x)
        # print(node_y)

        fig = go.Figure(data=[go.Sankey(
            node=dict(
                label=label,
                color = node_colors + px.colors.qualitative.Light24
                # x = node_x,
                # y = node_y,

            ),
            link=dict(
                source = source,
                target = target,
                value = value,
                color = color
            )
        )])
        #color = "#1db954"
        fig.update_layout(title_text=" Sankey plot for chosen artist ", font_size=18)

        st.plotly_chart(fig)