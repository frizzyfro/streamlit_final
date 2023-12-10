import streamlit as st
import random
import altair as alt
import numpy as np
import pandas as pd
from numpy.random import randint
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

data = pd.read_csv = ('jeff_jackson.csv')

# Assuming 'data' is your DataFrame
# Convert 'contribution_receipt_date' to datetime and ensure 'contribution_receipt_amount' is numeric
data['contribution_receipt_date'] = pd.to_datetime(data['contribution_receipt_date'], errors='coerce')
data['contribution_receipt_amount'] = pd.to_numeric(data['contribution_receipt_amount'], errors='coerce')

# Drop rows with invalid dates or amounts
valid_data = data.dropna(subset=['contribution_receipt_date', 'contribution_receipt_amount'])

# Aggregate data by date (summing the amounts)
grouped_data = valid_data.groupby('contribution_receipt_date')['contribution_receipt_amount'].sum().reset_index()

# Create a line chart
plt.figure(figsize=(12, 6))
plt.plot(grouped_data['contribution_receipt_date'], grouped_data['contribution_receipt_amount'], marker='o', linestyle='-')
plt.title('Total Receipt Amount Over Time')
plt.xlabel('Receipt Date')
plt.ylabel('Total Receipt Amount')
plt.xticks(rotation=45)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())

plt.show()



