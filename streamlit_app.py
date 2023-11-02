import streamlit as st
from utils.utils import plot_data

import pandas as pd
import numpy as np
import datetime

import matplotlib.pyplot as plt
import seaborn as sns


st.title('Crypto indicators')

PATH_DATA = 'Data/Formatted/btcusd_fmttd.csv'
PAIRS = ['BTC/USD']

# Load data
df = pd.read_csv(PATH_DATA, index_col='Time')
str_index = df.index
datetime_index = pd.to_datetime(str_index)

# Show data
st.write(f'The data we are working with is {PAIRS[0]},\
	which goes from {datetime_index.year.values[0]} to {datetime_index.year.values[-1]}.')

# Select a period of time
st.sidebar.write('Select data range')
init_time = st.sidebar.date_input(label='Initial date:',
	value=datetime.datetime(2020, 10, 29, 14, 30, 00),
	min_value=pd.to_datetime(df.index.values[0]),
	max_value=pd.to_datetime(df.index.values[-2]))
final_time = st.sidebar.date_input(label='Last date:',
	value=datetime.datetime(2020, 10, 30, 14, 30, 00),
	min_value=pd.to_datetime(df.index.values[1]),
	max_value=pd.to_datetime(df.index.values[-1]))

init_time = init_time.strftime('%Y-%m-%d %H:%M:%S')
final_time = final_time.strftime('%Y-%m-%d %H:%M:%S')


@st.cache_data
def select_data(init_time, final_time):
	"""
	Function to select data in period [init_time, final_time]
	"""
	return df.loc[init_time:final_time, :]

# Select data
df_day = select_data(init_time, final_time)

# Show selected data
show_selected_data = st.sidebar.checkbox(label='Show selected data', value=False)
if show_selected_data:
	st.write(df_day.loc[:, :'volume'])
else:
	st.write('To start, select the data range in the left sidebar.')


# PLOT
# ============================================
plot_bb_bands = True

# Show plot
plot_selected_data = st.sidebar.checkbox(label='Plot data', value=False)
if plot_selected_data:
	st.write('Plot of the data in the selected period:')
	fig = plot_data(df_day, plot_bb_bands)
	st.pyplot(fig=fig)
