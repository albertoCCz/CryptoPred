import numpy as np
import pandas as pd 

import matplotlib.pyplot as plt

import streamlit as st

def ob_os_areas(df):
	"""
	This function calculates the overbought and oversold
	areas from indicators K, D, J. The definition of each
	area is:

	Overbought area: K > 80, D > 70, J > 90
	Oversold area: K < 20, D < 30

	:param df:	dataframe
	:output:	array with the indices of area limits
	"""

	overbought_condition = (df['K'] > 80) & (df['D'] > 70) & (df['J'] > 90)
	oversold_condition = (df['K'] < 20) & (df['D'] < 30)
	    
	def lims(array):
	    lims = [[0,0]]
	    for idx, value in enumerate(array):
	        if (value == True) & (idx > lims[-1][-1]):
	            index = idx + 1
	            while index <= (len(array) - 1):
	                if array[index] == True:
	                    index += 1
	                else:
	                    break
	            if idx < (index - 1):
	                lims.append([idx, index-1])

	    return lims[1:]

	# Indexes of overbought and oversold limit areas
	ob_lims_id = lims(overbought_condition.values)
	os_lims_id = lims(oversold_condition.values)

	# Time of overbought and oversold limit areas
	ob_in_interval = df.index.values[np.isin(np.arange(len(df)), ob_lims_id)]
	os_in_interval = df.index.values[np.isin(np.arange(len(df)), os_lims_id)]

	return ob_in_interval, os_in_interval

def plot_data(df, plot_bb_bands=True):
	"""
	This function plots the closing price of the pair and also
	some indicators.

	:param df:				dataframe
	:param plot_bb_bands:	bool - wheather to plot Bollinger bands or not
	"""

	# Find the overbought and oversold area limits
	ob_in_interval, os_in_interval = ob_os_areas(df)

	# Create plot figure and axes
	fig, axes = plt.subplots(3, 1, sharex=True, figsize=(12,9), gridspec_kw={'height_ratios': [3, 1, 1]})

	# Global figure conditions
	plt.xticks(rotation=30)

	# Plot BTC/USD graph and indicators: sma, ema
	axes[0].plot(df.index, df['close'], linewidth=1.5, label='btc/usd')
	axes[0].plot(df.index, df['sma_3h'], linewidth=1.2, label='sma 3h')
	axes[0].plot(df.index, df['sma_6h'], linewidth=1.2, label='sma 6h')
	axes[0].plot(df.index, df['ema_6h'], linewidth=1.2, label='ema 6h')
	if plot_bb_bands:
	        axes[0].fill_between(df.index, df['upper_bb'], df['lower_bb'],
	                             color='cornflowerblue', alpha=0.3,
	                             linewidth=0.6, label='Boll')
	axes[0].legend()
	axes[0].set_ylabel('Close price [$]')
	axes[0].set_title(f'BTC/USD')
	axes[0].grid()

	# Plot indicator: rsi
	axes[1].plot(df.index, df['rsi'], linewidth=1.2, label='rsi')
	axes[1].plot(df.index, [70] * len(df.index), 'r--', linewidth=0.9, label='overbought')
	axes[1].plot(df.index, [30] * len(df.index), 'g--', linewidth=0.9, label='oversold')
	axes[1].set_ylabel('rsi')
	axes[1].set_ylim([0,100])
	axes[1].set_yticks([0, 30, 70, 100])
	axes[1].grid()

	# Plot indicator: KDJ and overbought and oversold areas
	axes[2].plot(df.index, df['K'], linewidth=1.2, label='K')
	axes[2].plot(df.index, df['D'], linewidth=1.2, label='D')
	axes[2].plot(df.index, df['J'], linewidth=1.2, label='J')
	axes[2].set_ylabel('KDJ')
	axes[2].set_xlabel('Time')
	for lim in range(len(ob_in_interval)):
	    if (lim % 2 == 0) & ((lim + 1) < (len(ob_in_interval))):
	        axes[2].axvspan(ob_in_interval[lim], ob_in_interval[lim+1], color='red', alpha=0.4)
	for lim in range(len(os_in_interval)):
	    if (lim % 2 == 0) & ((lim + 1) < (len(os_in_interval))):
	        axes[2].axvspan(os_in_interval[lim], os_in_interval[lim+1], color='green', alpha=0.4)
    
	axes[2].set_xticks(df.index.values[np.round(np.linspace(0, len(df.index.values) - 1, 6)).astype(int)])
	axes[2].grid()

	return fig
