import gbmplus
from datetime import datetime

# Submit a buy market order 

def main():        
    # Instantiate trader object
    gbm = gbmplus.GBMPlusAPI(output_log=False)
    
    # Get Strategy account
    swensen_strategy = gbm.accounts.getAccount("Swensen") # Replace with your strategy name
    
    # Get Legacy contract id from your strategy
    legacy_contract_id = swensen_strategy.get('legacy_contract_id')    


    # Generate an order object. (dict)
    order_object = gbm.orders.generateOrderObject(
        legacy_contract_id = legacy_contract_id,
        issuer = 'FUNO 11', # Replace Ticker here
        quantity = 1, # Replace Quantity here
        order_type = gbmplus.OrderTypes.Buy,
        trading_type = gbmplus.TradingTypes.Market,
        instrument_type = gbmplus.InstrumentTypes.SIC         
    )

    print("Order object to submit:", order_object)
    print("Submitting order...")
    
    #Submit order, speficy duration (in days)
    order = gbm.orders.submitOrder(legacy_contract_id, duration=1, order=order_object)
    print(order)

        
if __name__ == '__main__':
    start_time = datetime.now()
    main()
    end_time = datetime.now()
    print(f'\nScript complete, total runtime {end_time - start_time}')
