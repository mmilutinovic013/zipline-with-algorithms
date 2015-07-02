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

def initialize(context):
	context.security = symbol('AAPL')
	context.daycounter = 0

def handle_data(context, data):
	average_price = data[context.security].mavg(5)
	current_price = data[context.security].price
	cash = context.portfolio.cash

	if current_price > 1.05*average_price and cash > current_price:
		number_of_shares = int(cash/current_price)
		order(context.security, +number_of_shares)
        log.info("Buying %s" % (context.security.symbol))
    elif current_price < average_price and context.daycounter > 30:
            # Sell all of our shares by setting the target position to zero
        order_target(context.security, 0)
        log.info("Selling %s" % (context.security.symbol))
    
    # You can use the record() method to track any custom signal. 
    # The record graph tracks up to five different variables. 
    # Here we record the Apple stock price.
    record(stock_price=data[context.security].price)