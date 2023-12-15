import streamlit as st
import altair as alt
import numpy as np
import pandas as pd
from numpy.random import randint
import statistics 

data = pd.read_csv('dan_bishop.csv')

# Data preparation
data['contribution_receipt_date'] = pd.to_datetime(data['contribution_receipt_date'], errors='coerce')
data['contribution_receipt_amount'] = pd.to_numeric(data['contribution_receipt_amount'], errors='coerce')
data = data.dropna(subset=['contribution_receipt_date', 'contribution_receipt_amount', 'entity_type_desc'])

st.set_page_config(
    page_title="Dan Bishop",
    page_icon="🐘",
)

st.markdown("""
    <style>
    .font {
        font-size:30px;   # You can adjust the size as needed
    }
    </style>
    <div class='font'>
        Dan Bishop 🐘
    </div>
    """, unsafe_allow_html=True)



tab1, tab2 = st.tabs(["Contributions", "Largest Donors"])
with tab1:
    def calculate_total_contributions(data):
        total_contributions = sum(data)
        return total_contributions
    def avg_total_contributions(data):
        if len(data) == 0:
            return 0  # Handle the case when the data list is empty

        avg_contributions = sum(data) / len(data)
        return avg_contributions
    def med_total_contributions(data):
        if len(data) == 0:
            return None  # Handle the case when the data list is empty

        med_contributions = statistics.median(data)
        return med_contributions


    # Example data column
    data_column = data['contribution_receipt_amount']

    # Calculate total contributions
    total = calculate_total_contributions(data_column)
    avg = avg_total_contributions(data_column)
    median = med_total_contributions(data_column)

    # Display the title and total contributions in a Streamlit column
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric('Total Contributions:', '{:.2f}'.format(total))
    with col2:
        st.metric('Average Contributions', '{:.2f}'.format(avg))
    with col3:
        st.metric('Median Contributions', '{:.2f}'.format(median))

    # Year filter with checkboxes

    # Selector for entity_type_desc
    entity_type = st.selectbox('Select Entity Type', data['entity_type_desc'].unique())
    # Selector for year

    # Filter data based on selected entity type
    filtered_data = data[data['entity_type_desc'] == entity_type] 

    # Checkbox for toggling running totals
    show_running_totals = st.checkbox('Show Running Totals', value=False)

    # Calculate running totals if checkbox is checked
    if show_running_totals:
        filtered_data = filtered_data.sort_values('contribution_receipt_date')
        filtered_data['running_total'] = filtered_data.groupby('entity_type_desc')['contribution_receipt_amount'].cumsum()
        display_column = 'running_total'
    else:
        display_column = 'contribution_receipt_amount'

    # Aggregate data for line chart
    
    grouped_data = (filtered_data.groupby('contribution_receipt_date')[display_column]
                    .sum()
                    .reset_index())
    


    # Line chart
    line_chart = alt.Chart(grouped_data).mark_line(point=True).encode(
        x='contribution_receipt_date:T',
        y=f'{display_column}:Q',
        tooltip=['contribution_receipt_date', f'{display_column}']
    ).properties(
        width=700,
        height=400,
        title='Total Receipt Amount Over Time'
    )

    st.altair_chart(line_chart, use_container_width=True)

    # Top 10 contributors table
    top_contributors = (filtered_data.groupby('contributor_name')['contribution_receipt_amount']
                        .sum()
                        .sort_values(ascending=False)
                        .head(5)
                        .reset_index())

    st.header('Top 5 Contributors by Entity', divider='rainbow')

    st.table(top_contributors)

      

with tab2:
    st.header("Largest Donors")
    def find_max_contributor(data):
        # Ensure 'contribution_receipt_amount' is a numeric type
        data['contribution_receipt_amount'] = pd.to_numeric(data['contribution_receipt_amount'], errors='coerce')

        # Find the index of the max contribution
        idx_max_contribution = data['contribution_receipt_amount'].idxmax()

        # Retrieve the contributor with the max contribution
        max_contributor = data.loc[idx_max_contribution, 'contributor_name']
        max_value = data.loc[idx_max_contribution, 'contribution_receipt_amount']
        max_entity = data.loc[idx_max_contribution, 'entity_type_desc']

        return max_contributor, max_value, max_entity


    # Calculate total contributions
    max_contributor, max_value, max_entity = find_max_contributor(data)

    # Display the result using Streamlit
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"<h2 style='text-align:center; font-size:20px;'>Largest Contributor</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center; font-size:18px;'>{max_contributor}</p>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"<h2 style='text-align:center; font-size:20px;'>Contribution Amount</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center; font-size:18px;'>{max_value:.2f}</p>", unsafe_allow_html=True)

    with col3:
        st.markdown(f"<h2 style='text-align:center; font-size:20px;'>Contributor Type</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center; font-size:18px;'>{max_entity}</p>", unsafe_allow_html=True)

    
        # Aggregate data for top contributors
    top_contributors = (data.groupby(['contributor_name', 'entity_type_desc'])
                        .agg(total_contribution=('contribution_receipt_amount', 'sum'))
                        .reset_index()
                        .sort_values(by='total_contribution', ascending=False)
                        .head(10))  # Adjust number as needed

    # Bar chart
    chart = alt.Chart(top_contributors).mark_bar().encode(
        x=alt.X('total_contribution:Q', title='Total Contribution'),
        y=alt.Y('contributor_name:N', title='Contributor Name', sort='-x'),
        color='entity_type_desc:N'
    ).properties(
        title='Top Contributions by Contributor',
        width=800,
        height=700
    )

    chart