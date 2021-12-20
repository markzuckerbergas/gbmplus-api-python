import gbmplus
from datetime import datetime

# Submit a buy market order using Trading USA 

def main():        
    # Instantiate trader object
    gbm = gbmplus.GBMPlusAPI(output_log=False)
    ticker = "AMZN"
        
    t_usa = gbm.accounts.getAccount("Trading USA")
    t_usa_account_id = t_usa.get('account_id')

    # Get USA Markets. This operation takes a long time
    print("Getting USA Markets...")
    markets_USA = gbm.tradingUSA.getMarketsUSA()

    markets_dict = {element["security_id"]: element for element in markets_USA}
    amazon = markets_dict.get(ticker)
    
    # Get the instument_id 
    amazon_instrument_id = amazon.get("instrument_id")

    print("Generating USA Order")
    #Generate USA buy order for 20 MXN pesos
    USA_order = gbm.tradingUSA.generateOrderUSA(t_usa_account_id, ticker, 20, amazon_instrument_id)
    print(USA_order)

    print("Getting USA orders")
    #List recent orders
    orders = gbm.tradingUSA.getOrdersUSA(t_usa_account_id)
    print(orders)

        
if __name__ == '__main__':
    start_time = datetime.now()
    main()
    end_time = datetime.now()
    print(f'\nScript complete, total runtime {end_time - start_time}')