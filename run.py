import airtable
import pandas as pd
from datetime import timedelta
import numpy as np
import plotly.graph_objects as go

# Replace 'baseKey', 'tableName', and 'apiKeyValue' with appropriate values.
airtable = airtable.Airtable('baseKey', 'tableName', api_key='apiKeyValue')

# Retrieve all data from the 'Main View' and store it in 'table_data'
table_data = airtable.get_all(view="Grid view")

times = [x['fields']['time'] for x in table_data]
dates = [x['fields']['created_date'] for x in table_data]
datetimes = [x['createdTime'] for x in table_data]

df = pd.DataFrame(list(zip(datetimes, times, dates)), columns=['Datetime', 'Time', 'Date'])

df['Datetime'] = pd.to_datetime(df['Datetime'])

df['datetime_minus_5'] = df['Datetime'] - timedelta(hours=5)
df['Date'] = df['datetime_minus_5'].dt.date
df_clean = df.groupby('Date').max().reset_index()

df_clean['ten_pm'] = pd.to_datetime("1900-01-01 22:00:00+00:00")
df_clean['hour'] = df_clean['Time'].str[:2].to_string()

for i, row in df_clean.iterrows():
    if row['hour'] in ['00', '01', '02', '03', '04']:
        df_clean.at[i, 'ten_pm'] = pd.to_datetime(str(row['Date']) + " " + "22:00:00+00:00") - pd.DateOffset(1)   
    else:
        df_clean.at[i, 'ten_pm'] = pd.to_datetime(str(row['Date']) + " " + "22:00:00+00:00")

df_clean['hours after 10'] = (df_clean['datetime_minus_5'] - df_clean['ten_pm']) / np.timedelta64(1, 'h')
df_clean = df_clean.sort_values("Date", ascending=False).reset_index()
df_clean = df_clean[0:7]

df_clean['hours after 10'] = np.round(df_clean['hours after 10'], 2)
df_clean['bar_val'] = 10 + df_clean['hours after 10']

# remove values that don't make sense (i.e. are after 5am or before 6pm)
# in other words bar_val should be between 6 and 15
df_clean = df_clean[(df_clean.bar_val <= 15) & (df_clean.bar_val >= 6)]

colors = ['#d52c40' if val >= 0 else '#6cdae7' for val in df_clean['hours after 10'].tolist()]


# Create the bar chart
fig = go.Figure(data=[
    go.Bar(
        x=df_clean['Date'],
        y=df_clean['bar_val'],
        marker_color=colors
    )
])

mean_val = df_clean['hours after 10'].mean()
if mean_val > 0:
    title_val = "You can do better"
else:
    title_val = "Nice! You're going to bed on time!"

# Update layout
fig.update_layout(
    title={"text": title_val, 'font': {'size': 30}},
    xaxis_title={'text': 'Date', 'font': {'size': 18}},
    yaxis_title={'text': 'Bedtime', 'font': {'size': 18}},
    yaxis={
        'tickfont': {'size': 14} 
    },
    showlegend=False,
    template='simple_white'
)
fig.update_layout(yaxis_range=[0, 15])
fig.add_hline(y=10, line_width=3, fillcolor="black", opacity=.9)

# Show the plot
fig.write_image("figure.jpeg")
print('end of file')
