import json
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

df = pd.read_json("../Mg/StreamingHistory0.json")
df1 = pd.read_json("../Mg/StreamingHistory1.json")
df=df.append(df1,ignore_index=True).query("msPlayed>30000")
df["endTime"]=pd.to_datetime(df["endTime"])
df["weekday"] = df["endTime"].dt.day_name()
df["hour"] = df["endTime"].dt.hour
df["count"] = df.groupby(["hour","weekday"])["weekday"].transform('count')
cats = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
df['weekday'] = pd.Categorical(df['weekday'], categories=cats, ordered=True)
df = df.sort_values('weekday')
print(df.sample(5))
df.info()

df1 = df[['hour','weekday','count']]
x = pd.DataFrame(df1['weekday'].unique())
heatmap_pt = pd.pivot_table(df1,values ='count', index=['hour'], columns='weekday')
fig, ax = plt.subplots(figsize=(16,8))
sns.set()
sns.heatmap(heatmap_pt, cmap='YlGnBu')
plt.xticks(rotation=15)
plt.show()