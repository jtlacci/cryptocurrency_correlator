# cryptocurrency_correlator

Creates a heatmap that plots the correlation between a list of crypto currencies over a set timeperiod using 
data pulled from Poloniex API. 

Within the code you can change the start and end time as well as the candlestick period, coin names are pulled 
from coin.txt. The data is manipulated using Pandas and the chart is rendered with Matplotlib.

########Changelog#######

Added conversion from BTC to USD before calculations, BTC is now hardcoded and SHOULD NOT be added to coins.txt.

