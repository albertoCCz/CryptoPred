import streamlit as st

import pandas as pd
import numpy as np
import datetime

import matplotlib.pyplot as plt
import seaborn as sns


st.title('Crypto indicators')

PATH_DATA = 'Data/Formatted/btcusd_fmttd.csv'

# Load data
df = pd.read_csv(PATH_DATA, index_col='Time')

# Show data
st.write('Data we are working with:')
st.write(df.loc[:, :'volume'].head(5))

