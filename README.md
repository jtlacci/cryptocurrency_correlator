# cryptocurrency_correlator

Creates a heatmap that plots the correlation between a list of crypto currencies over a set timeperiod using 
data pulled from Poloniex API. Pulls data from Poloniex API between the start and end dates.

"Start" and "end" are given in UNIX timestamp format and used 
to specify the date range for the data returned.

Candlestick period in seconds; valid values are 300 (5 minutes), 900 (15 minutes), 1800 (30 minutes), 
7200 (2 hours), 14400 (4 hours), and 86400 (1 day)

Coin tickers are pulled from coin.txt. Datapoints are manipulated using Pandas and the chart is rendered with Matplotlib.

## Changelog

Added conversion from BTC to USD before calculations, BTC is now hardcoded and SHOULD NOT be added to coins.txt.

