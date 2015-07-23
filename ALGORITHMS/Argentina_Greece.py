# Market Analysis during a time of financial crisis:
# 
# The plan with this algorithm is that we hope to analyse the trends associated with a countries market 
# failure and try to find patterns to apply it to financial stock trading decisions in these times of crisis.
# 
#  For example: Argentina (much like Greece recently) defaulted on a payment which caused a massive depression
#  in their markets and hurt the economy. Argentina has certain products that it exports to multiple places in
#  the world, which were affected by this defaulting and subsequent recession. What I hope to discover from this
#  algorithm is to be able to read how critical goods of a country will be affected and if it is still practical
#  to keep stocks within this coutnries realm.
#  
#   Here are some categories of which to analyse:
#   
#    1) Agriculture
#    2) Mining
#    3) Manufacturing
#    4) Public Utilities
#    5) Construction
#    6) Commerce and Tourism
#    7) Transport and Communication
#    8) Financial Services
#    9) Real Estate
#    10) Public Administration / Defense
#    11) Health and Education
#    12) Other
#   
#   If we look at these sectors and their trends over a time of depression we will be able to look for
#   patterns to determine if this market is stable enough to invest in / what types of services would be most
#   likely to grow through the process of the depression. 
# This example runs the same momentum play as the first sample 
# (https://www.quantopian.com/help#sample-basic), but this time it uses more
# securities during the backtest.
    
# Important note: All securities in an algorithm must be traded for the 
# entire length of the backtest.  For instance, if you try to backtest both
# Google and Facebook against 2011 data you will get an error; Facebook
# wasn't traded until 2012.

# First step is importing any needed libraries.

import datetime
import pytz

def initialize(context):
    # Here we initialize each stock.
    context.stocks = symbols('BMA','TEO', 'TS', 'TGS')
    context.vwap = {}
    context.price = {}
 
    # Setting our maximum position size, like previous example
    context.max_notional = 1000000.1
    context.min_notional = -1000000.0

    # Initializing the time variables we use for logging
    # Convert timezone to US EST to avoid confusion
    est = pytz.timezone('US/Eastern')
    context.d=datetime.datetime(2000, 1, 1, 0, 0, 0, tzinfo=est)
    context.daycounter = 0

def handle_data(context, data):
    # We add a new day each time we iterate through this function...
    cash = context.portfolio.cash
    context.daycounter += 1
    for stock in context.stocks:
        average_price = data[stock].mavg(5)
        current_price = data[stock].price
        tradeday = data[stock].datetime
        if current_price > 1.03*average_price and cash > current_price:
            number_of_shares = int(cash/current_price)
            # Place the buy order (positive means buy, negative means sell)
            order(stock, +number_of_shares)
            log.info("Buying %s" % (stock))
        
    if (context.d + datetime.timedelta(days=1)) < tradeday:
        context.d = tradeday