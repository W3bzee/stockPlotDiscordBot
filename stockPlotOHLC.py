# Import Packages
from distutils.log import info
from itertools import count
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

## DEFINE FUNCTIONS
def getHistoricalStockData(ticker):
    stock = yf.Ticker(ticker)
    # get historical market data
    hist = stock.history(period="max")
    historicalDF = pd.DataFrame(hist)
    timeframe = getTimeFrame(historicalDF)
    return historicalDF.loc[historicalDF.index[:].isin(timeframe)]

def getCurrentStockData(ticker):
    stock = yf.Ticker(ticker)
    current_price = stock.info['currentPrice']    
    peg_ratio = stock.info['pegRatio']
    forward_pe = stock.info['forwardPE']
    

    return f'{ticker} \n\
    Current price: {current_price} $USD \n\
    PEG Ratio: {peg_ratio} \n\
    Forward PE: {forward_pe}'

def getTimeFrame(dataFrameInput):
    #userSelection = input('What Timeframe are you interested in? \n Select: \n\
    #0: 1 Week \n\
    #1: 1 Month \n\
    #2: 3 Months \n\
    #3: 6 Months \n')
    userSelection = '1'
    timeFrameDict = {'0':7,'1':30,'2':90,'3':180}
    days = timeFrameDict[userSelection]
    x = dataFrameInput.index[:]
    timeframe = x[len(x)-days:len(x)]
    return timeframe

def ohlcPlot(indexedDF,tick):
    #Define Plot Sizes

    plt.style.use('dark_background')
    fig, (ax, ax2) = plt.subplots(2, figsize=(12,8), gridspec_kw={'height_ratios': [4, 1]})
    counter = 0
    xSeries = list(indexedDF.index[:])
    # Make OHLC CHART
    for idx, val in indexedDF.iterrows():
        color = '#2CA453'
        if val['Open'] > val['Close']: color= '#F04730'
        ax.plot([xSeries[counter], xSeries[counter]], [val['Low'], val['High']], color = color)
        # open marker
        ax.plot([xSeries[counter], xSeries[counter]-timedelta(hours=8)], [val['Open'], val['Open']], color=color)
        # close marker
        ax.plot([xSeries[counter], xSeries[counter]+timedelta(hours=8)], [val['Close'], val['Close']], color=color)
        counter +=1

    #YLABELS
    ax.set_ylabel('USD $',fontsize = 'xx-large')
    ax2.set_ylabel('Volume',fontsize = 'xx-large')

    #GRID
    ax.xaxis.grid(color='white', linestyle='dashed', which='both', alpha=0.5)
    ax.yaxis.grid(color='white', linestyle='dashed', which='both', alpha=0.5)
    ax2.set_axisbelow(True)
    ax2.yaxis.grid(color='white', linestyle='dashed', which='both', alpha=0.5)

    #PLOT VOLUME BARS
    ax2.bar(xSeries, indexedDF['Volume'], color='lightgrey')
    # get max volume + 10%
    mx = indexedDF['Volume'].max()*1.1
    # define tick locations - 0 to max in 4 steps
    yticks_ax2 = np.arange(0, mx+1, mx/4)
    # create labels for ticks. Replace 1.000.000 by 'mi'
    yticks_labels_ax2 = ['{:.1f} mil'.format(i/1000000) for i in yticks_ax2]
    ax2.yaxis.tick_right() # Move ticks to the left side
    # plot y ticks / skip first and last values (0 and max)
    plt.yticks(yticks_ax2[1:-1], yticks_labels_ax2[1:-1])
    plt.ylim(0,mx)


    ax.text(1.0, 0.0, 'Created by W3bzee', transform=ax.transAxes,
        fontsize=22, color='red', alpha=0.5,
        ha='right', va='bottom', rotation='0')

    #TITLE
    ax.set_title('{} Candlestick Chart\n'.format(tick), loc='left', fontsize=20)
    # no spacing between the subplots
    plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig('Graphs/{}.png'.format(tick))
    #plt.show()
    return


# Call this function with a Stock Ticker to output the Chart to the Graphs Folder
def StockGraph(Ticker):
    dataset = getHistoricalStockData(Ticker)
    ohlcPlot(dataset,Ticker)
    

#tick = 'AAPL'
#stock = yf.Ticker(tick)
# show actions (dividends, splits)
#stock.actions
# show dividends
#stock.dividends
# show splits
#stock.splits
# show financials
#stock.financials
#print(stock.quarterly_financials)

# show major holders
#stock.major_holders
#print(stock.major_holders)
# show institutional holders
#stock.institutional_holders
# show balance sheet
#stock.balance_sheet
#stock.quarterly_balance_sheet
# show cashflow
#stock.cashflow
#stock.quarterly_cashflow
# show earnings
#stock.earnings
#stock.quarterly_earnings
# show sustainability
#stock.sustainability
# show analysts recommendations
#stock.recommendations
# show next event (earnings, etc)
#stock.calendar
# show all earnings dates
#stock.earnings_dates
# show ISIN code - *experimental*
# ISIN = International Securities Identification Number
#stock.isin
# show options expirations
#stock.options
# show news
#stock.news
# get option chain for specific expiration
#opt = stock.option_chain('2022-07-22')
# data available via: opt.calls, opt.puts

