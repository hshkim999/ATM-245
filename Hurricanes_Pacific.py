import numpy as np
import pandas as pd
import seaborn
import matplotlib.pyplot as plt
import plotly.express as px

import os
for dirname, _, filenames in os.walk('/Users/harrykim/Downloads/archive'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

pacific_hurricanes = pd.read_csv('/Users/harrykim/Downloads/archive/pacific.csv')
pacific_hurricanes.head
df = pd.DataFrame(pacific_hurricanes)
df.shape

booleans =[]
for date in df['Date']:
    if date > 19500000:
        booleans.append(True)
    else:
        booleans.append(False)
date_range = pd.Series(booleans)
new_df = df[date_range]
new_df.shape
new_df

new_df.drop(['ID', 'Time', 'Name', 'Minimum Pressure', 'Event'], axis = 1)
new_df['Longitude'] = new_df['Longitude'].map(lambda x: x.rstrip('W'))
new_df['Latitude'] = new_df['Latitude'].map(lambda x: x.rstrip('N'))
new_df['Latitude'] = new_df['Latitude'].map(lambda x: x.rstrip('S'))
new_df['Longitude'] = new_df['Longitude'].map(lambda x: x.rstrip('E'))
new_df
new_df['Latitude'] = new_df['Latitude'].astype(float)
new_df['Longitude'] = new_df['Longitude'].astype(float)
lat_filtered_df = new_df[(new_df['Latitude'].astype(float) >= float(7)) & (new_df['Latitude'].astype(float) <= float(24))]
print(lat_filtered_df.shape)
lat_filtered_df['Longitude'] = (lat_filtered_df['Longitude'] * -1)
lat_long_filtered_df = lat_filtered_df[(lat_filtered_df['Longitude'] >= -105) & (lat_filtered_df['Longitude'] <= float(-60))]
print(lat_long_filtered_df.shape)

all_columns = list(lat_long_filtered_df)
lat_long_filtered_df[all_columns] = lat_long_filtered_df[all_columns].astype(str)
lat_long_filtered_df = lat_long_filtered_df.replace('-999', np.nan)
lat_long_filtered_df = lat_long_filtered_df.replace('-99', np.nan)
lat_long_filtered_df

lat_long_filtered_df['Date'] = pd.to_datetime(lat_long_filtered_df['Date'].astype(str), format = '%Y %m %d')
lat_long_filtered_df
lat_long_filtered_df['Year'] = lat_long_filtered_df['Date'].map(lambda x: x.year)
lat_long_filtered_df

negatives =[]
for i in lat_long_filtered_df['Maximum Wind']:
    if float(i) < 0:
        negatives.append(i)

print(negatives)

lat_long_filtered_df = lat_long_filtered_df.sort_values(by='Maximum Wind', ascending=False)
lat_long_filtered_df = lat_long_filtered_df.drop_duplicates(subset='Name', keep="first")
lat_long_filtered_df = lat_long_filtered_df.sort_values(by ='Year', ascending = True)
print(lat_long_filtered_df.shape)
lat_long_filtered_df
print(179/23)

number_of_storms={}
count = lat_long_filtered_df['Year'].value_counts()
count_df = pd.DataFrame(count)
count_df = count_df.reset_index()
count_df = count_df.rename(columns={"index": "Year", "Year": "Count"})
count_df = count_df.sort_values(by = "Year", ascending = True)
count_df

lat_long_filtered_df['Maximum Wind'] = lat_long_filtered_df['Maximum Wind'].astype(float)
lat_long_filtered_df.Year = lat_long_filtered_df.Year.astype(int)
grouped_df = lat_long_filtered_df.groupby(['Year'])
described_df = grouped_df.describe()
described_df = described_df.reset_index()
described_df = pd.DataFrame(described_df)
described_df.columns = ['Year', 'Count', "Mean", 'std', 'min', '25%', '50%', '75%', 'Max']
described_df
described_df

month_df = lat_long_filtered_df
month_df = month_df.drop(['Year'], axis=1)
month_df['Month'] = month_df['Date'].map(lambda x: x.month)

month_df['Maximum Wind'] = month_df['Maximum Wind'].astype(float)
month_df.Month = month_df.Month.astype(int)

grouped_df_month = month_df.groupby(['Month'])
described_df_month = grouped_df_month.describe()
described_df_month = described_df_month.reset_index()
described_df_month= pd.DataFrame(described_df_month)
described_df_month.columns = ['Month', 'Count', "Mean", 'std', 'min', '25%', '50%', '75%', 'Max']
described_df_month

from textwrap import wrap
named_colorscales = px.colors.named_colorscales()
print("\n".join(wrap("".join('{:<12}'.format(c) for c in named_colorscales), 96)))
fig_1 = px.bar(described_df,
                 x= 'Year',
                 y='Count',
                 color = 'Mean',
                 color_continuous_scale=px.colors.sequential.OrRd,
                 title = 'Frequency and Average Wind Speed <br>of Large Storms in Pacific (1950-2015)',
                 labels={'Count':'Number of Large Storms', 'Mean' : 'Average Wind <br> Speed (knots)'}
                )
fig_1.update_layout(title_x=0.5)
fig_1.show()

fig_2 = px.bar(described_df_month,
                 x= 'Month',
                 y='Count',
                 color = 'Mean',
                 color_continuous_scale=px.colors.sequential.OrRd,
                 title = 'Frequency and Average Max. Wind Speed <br> of Large Storms in Pacific by Month <br> (1950-2015) <br>',
                 text = 'Mean',
                 labels={'Count':'Number of Large Storms', 'Mean' : 'Average Maximum <br> Wind Speed (knots)'}
                )
fig_2.update_layout(
                    title_x=0.5,
                    xaxis = dict(
        tickmode = 'array',
        tickvals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        ticktext = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                                )
                    )
fig_2.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig_2.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
fig_2.show()



import plotly.graph_objects as go

fig = go.Figure(data=go.Scattergeo(

    lat = lat_long_filtered_df['Latitude'],
    lon = lat_long_filtered_df['Longitude'],

)
                )
fig.update_geos(
    center=dict(lon=-90, lat= 15),
    lataxis_range=[7, 24], lonaxis_range=[-105, -60]
                )

fig.show()


fig_num = px.bar(count_df,
                 x='Year',
                 y='Count',
                 title = 'Number of Large Storms in Pacific by Year (1950-2015)',
                 labels={'Count':'Number of Large Storms'}
                )

fig_num.update_layout(title_x=0.5)
fig_num.show()
