# 
# The goal for this algorithm is going to be to run a few tests on different market parameters to
# determine what kind of market we are looking at (eg. given a new market)
# 
# This will help with short term and long term market analysis, and teach the program what market it is looking
# at. For the user it makes it simple to make investment decisions and allows them to make important decisions 
# on if new markets look like they are good ones to enter or not. 
# 
# We will look at a tech market, a failed market, and a natural resource market for these tests.
# 
# Based on the result we will teach the program what decisions are best to make as long as it chose the
# correct market fromt the data.
# 
# Another feature to add will be a function that says the market is indetermiable at the moment, saying it needs
# more data. This will allow the risk to be calculated so that the program doesn't make rash decisions costing the
# user a lot of money.
#
# To run an algorithm in Quantopian, you need two functions: 
# initialize and handle_data.
def initialize(context):
    # The initialize function sets any data or variables that 
    # you'll use in your algorithm. 
    # For instance, you'll want to define the security 
    # (or securities) you want to backtest.  
    # You'll also want to define any parameters or values 
    # you're going to use later. 
    # It's only called once at the beginning of your algorithm.
    
    # In our example, we're looking at Apple.  
    # If you re-type this line you'll see 
    # the auto-complete that is available for security. 
    context.security = symbol('AAPL')
    # initialize a day counter so that days can be taken into account 
    context.daycounter = 0
    #comment

# The handle_data function is where the real work is done.  
# This function is run either every minute 
# (in live trading and minute backtesting mode) 
# or every day (in daily backtesting mode).
def handle_data(context, data):
    # We add a new day each time we iterate through this function...
    context.daycounter += 1
    # We've built a handful of useful data transforms for you to use,
    # such as moving average. 
    # To make market decisions, we're calculating the stock's 
    # moving average for the last 5 days and its current price. 
    average_price = data[context.security].mavg(5)
    current_price = data[context.security].price
    
    # Another powerful built-in feature of the Quantopian backtester is the
    # portfolio object.  The portfolio object tracks your positions, cash,
    # cost basis of specific holdings, and more.  In this line, we calculate
    # the current amount of cash in our portfolio. 
    cash = context.portfolio.cash
    
    # Here is the meat of our algorithm.
    # If the current price is 1% above the 5-day average price 
    # AND we have enough cash, then we will order.
    # If the current price is below the average price, 
    # then we want to close our position to 0 shares.
    if current_price > 1.03*average_price and cash > current_price and context.daycounter > 3:
        
        # Need to calculate how many shares we can buy
        number_of_shares = int(cash/current_price)
        
        # Place the buy order (positive means buy, negative means sell)
        order(context.security, +number_of_shares)
        log.info("Buying %s" % (context.security.symbol))
        # if we are successful in buying shares we reset the day counter to
        # measure our success for the next month...
        context.daycounter = 0

    # if the current price is lower than the average price for more than 30 days...
    # We sell all of our stocks, because the price is probably tanking too much.
    elif current_price < average_price and context.daycounter > 30:  
        # Sell all of our shares by setting the target position to zero
        order_target(context.security, 0)
        log.info("Selling %s" % (context.security.symbol))
    
    # You can use the record() method to track any custom signal. 
    # The record graph tracks up to five different variables. 
    # Here we record the Apple stock price.
    record(stock_price=data[context.security].price)