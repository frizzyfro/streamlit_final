import streamlit as st
import altair as alt
import numpy as np
import pandas as pd
from numpy.random import randint
import statistics 

st.set_page_config(
    page_title="Attorney General Candidates Details",
    page_icon="⚖️",
)

st.write("# Candidate Information: ⚖️")

st.sidebar.success("Click on different candidates above")

import pandas as pd
import altair as alt

# Load the data from the CSV files
data = pd.read_csv('jeff_jackson.csv')
data1 = pd.read_csv('dan_bishop.csv')

# Assign the 'Dataset' column to each dataset
data['Dataset'] = 'Jeff Jackson'
data1['Dataset'] = 'Dan Bishop'

# Combining the two datasets
combined_data = pd.concat([data, data1])

# Creating a line chart
chart = alt.Chart(combined_data).mark_line().encode(
    x='contribution_receipt_date:T',  # T indicates temporal (date/time) data
    y='contribution_receipt_amount:Q',  # Q indicates quantitative data
    color=alt.Color('Dataset:N', scale=alt.Scale(  # N indicates nominal (categorical) data
        domain=['Jeff Jackson', 'Dan Bishop'],
        range=['blue', 'red']
    )),
    tooltip=[alt.Tooltip('contribution_receipt_date:T', title='Date'),
        alt.Tooltip('contribution_receipt_amount:Q', title='Amount'),
        alt.Tooltip('Dataset:N', title='Candidate')]
).properties(
    width=800,
    height=400,
    title='Contribution Receipt Amount Over Time'
)

# Display the chart
chart

# Aggregating the data
agg_data = combined_data.groupby(['entity_type_desc', 'Dataset']).agg(
    total_contribution=('contribution_receipt_amount', 'sum')).reset_index()

# Creating a grouped bar chart
chart = alt.Chart(agg_data).mark_bar().encode(
    x=alt.X('entity_type_desc:N', title='Entity Type'),  # x-axis shows entity type
    y=alt.Y('total_contribution:Q', title='Contribution Receipt Amount'),  # y-axis shows summed contribution amount
    color=alt.Color('Dataset:N', scale=alt.Scale(  # N indicates nominal (categorical) data
        domain=['Jeff Jackson', 'Dan Bishop'],
        range=['blue', 'red']
    )),
    tooltip=[
        alt.Tooltip('entity_type_desc:N', title='Entity Type'),
        alt.Tooltip('total_contribution:Q', title='Total Contribution'),
        alt.Tooltip('Dataset:N', title='Candidate')]
).properties(
    width=800,
    height=400,
    title='Comparison of Contributions by Entity Type'
)

# Display the chart
chart


# Aggregating the data and getting the top 10 states for each dataset
agg_data = combined_data.groupby(['contributor_state', 'Dataset']).agg(
    total_contribution=('contribution_receipt_amount', 'sum')
).reset_index()

# Sorting and keeping the top 10 states for each dataset
top_states_data = (agg_data.sort_values(['Dataset', 'total_contribution'], ascending=[True, False])
                   .groupby('Dataset')
                   .head(10))

# Creating a horizontal, unstacked bar chart
chart = alt.Chart(top_states_data).mark_bar().encode(
    y=alt.Y('contributor_state:N', title='State'),  # y-axis shows states
    x=alt.X('total_contribution:Q', title='Total Contribution Amount'),  # x-axis shows summed contribution amount
    color='Dataset:N',  # Color encoding for different datasets
    column='Dataset:N',  # Place bars from different datasets next to each other
    tooltip=[alt.Tooltip('contributor_state:N', title='State'),
             alt.Tooltip('total_contribution:Q', title='Total Contribution'),
             alt.Tooltip('Dataset:N', title='Dataset')]
).properties(
    title='Top 10 Contributions by State for Each Dataset'
)

# Display the chart
chart


# # Aggregating the data
agg_data = combined_data.groupby(['contributor_state', 'Dataset']).agg(
    total_contribution=('contribution_receipt_amount', 'sum')
).reset_index()

# Getting the top 10 states for each dataset
top_states_dataset1 = agg_data[agg_data['Dataset'] == 'Dataset 1'].nlargest(10, 'total_contribution')
top_states_dataset2 = agg_data[agg_data['Dataset'] == 'Dataset 2'].nlargest(10, 'total_contribution')

# Combine top states from both datasets
top_states_combined = pd.concat([top_states_dataset1, top_states_dataset2])

# Creating a horizontal bar chart
chart = alt.Chart(top_states_combined).mark_bar().encode(
    y=alt.Y('contributor_state:N', title='State'),  # y-axis shows states
    x=alt.X('total_contribution:Q', title='Total Contribution Amount'),  # x-axis shows summed contribution amount
    color='Dataset:N',  # Color encoding for different datasets
    tooltip=[alt.Tooltip('contributor_state:N', title='State'),
             alt.Tooltip('total_contribution:Q', title='Total Contribution'),
             alt.Tooltip('Dataset:N', title='Dataset')]
).properties(
    title='Top 10 Contributions by State for Each Dataset'
)

# Display the chart
chart