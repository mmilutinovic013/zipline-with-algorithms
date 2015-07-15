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
   

def handle_data(context, data):
    # Initializing the position as zero at the start of each frame
    notional=0
    
    # This runs through each stock.  It computes
    # our position at the start of each frame.
    for stock in context.stocks:
        price = data[stock].price 
        notional = notional + context.portfolio.positions[stock].amount * price
        tradeday = data[stock].datetime
        
    # This runs through each stock again.  It finds the price and calculates
    # the volume-weighted average price.  If the price is moving quickly, and
    # we have not exceeded our position limits, it executes the order and
    # updates our position.
    for stock in context.stocks:   
        vwap = data[stock].vwap(3)
        record(arg_mavg=data[data[stock]].mavg(20))
        price = data[stock].price  

        if price < vwap * 0.995 and notional > context.min_notional:
            order(stock,-100)
            notional = notional - price*100
        elif price > vwap * 1.005 and notional < context.max_notional:
            order(stock,+100)
            notional = notional + price*100

    # If this is the first trade of the day, it logs the notional.
    if (context.d + datetime.timedelta(days=1)) < tradeday:
        log.debug(str(notional) + ' - notional start ' + tradeday.strftime('%m/%d/%y'))
        context.d = tradeday