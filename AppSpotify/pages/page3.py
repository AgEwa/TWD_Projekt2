import datetime
from datetime import date

import clr as clr
import pandas as pd
import seaborn as sns
import streamlit as st
from matplotlib import pyplot as plt
import matplotlib as mpl
import matplotlib.colors as clr
from matplotlib.colors import ListedColormap

st.title("When and what do we listen to most often?")
data = st.radio("Which data to display?", ["MyData", "Mg"])

#start = st.date_input("Enter the start date")
#end = st.date_input("Enter the end date")

df = pd.read_json("./" + data + "/StreamingHistory0.json")
df1 = pd.read_json("./" + data + "/StreamingHistory1.json")
df = df.append(df1, ignore_index=True).query("msPlayed>30000")
df["endTime"] = pd.to_datetime(df["endTime"])
#df = df.loc[(df['endTime']>=start) & (df['endTime']<=end)]

start = st.date_input("Enter the start date",min_value=df["endTime"].min(),
                      max_value=df["endTime"].max(), value=df["endTime"].min())
end = st.date_input("Enter the end date",min_value=df["endTime"].min(),
                      max_value=df["endTime"].max(), value=df["endTime"].max())

df= df.loc[(df["endTime"].dt.date>start) &(df["endTime"].dt.date<end)]
df["weekday"] = df["endTime"].dt.day_name()
df["hour"] = df["endTime"].dt.hour
df["count"] = df.groupby(["hour", "weekday"])["weekday"].transform('count')
cats = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
df['weekday'] = pd.Categorical(df['weekday'], categories=cats, ordered=True)
df = df.sort_values('weekday')

#df.info()

df1 = df[['hour', 'weekday', 'count']]
x = pd.DataFrame(df1['weekday'].unique())
heatmap_pt = pd.pivot_table(df1, values='count', index=['hour'], columns='weekday')
fig, ax = plt.subplots(figsize=(16, 8))
sns.set(rc={'axes.facecolor':"#191414", 'figure.facecolor':"#191414"})
mpl.rcParams.update({'text.color' : "white",
                     'axes.labelcolor' : "white",
                     'legend.labelcolor': "white",
                     'legend.edgecolor':"white",
                     'legend.facecolor':"white",
                     'xtick.color':"white",
                     'ytick.color':"white"})
#gyr = ['#28B463','#FBFF00', '#C0392B']
#my_colors = ListedColormap(sns.color_palette(gyr))     201A1A      2CFF77
#cmap=sns.cubehelix_palette(start=2, rot=0, dark=0, light=.95, reverse=True, as_cmap=True)
my_colors = clr.LinearSegmentedColormap.from_list('custom blue', ['#201A1A','#0ABD4A','#A2FFC4'], N=256)
sns.heatmap(heatmap_pt, cmap=my_colors)
plt.xticks(rotation=15)




#st.write(a)
st.pyplot(fig)
