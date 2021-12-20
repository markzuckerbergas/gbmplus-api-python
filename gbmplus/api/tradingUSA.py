class TradingUSA(object):
    def __init__(self, session):
        super(TradingUSA, self).__init__()
        self._session = session
                

    def generateOrderUSA(self, account_id, issuer, amount, instrument_id, order_type="buy"):
        """
        **Generate an Order in the Trading USA platform**
        https://api.trading-usa.gbm.com/v1/orders/contracts/{main_contract_id}/accounts/{account_id}/orders

        - account_id (string): (required)
        - issuer (string): (required)
        - amount (float): (required)                
        - instrument_type (required)        
        """
        
        metadata = {
            'tags': ['orderUSA', 'Trading USA'],
            'operation': 'generateOrderUSA'
        }
                
        main_contract_id = self._session._main_contract_id
        
        resource = f"https://api.trading-usa.gbm.com/v1/orders/contracts/{main_contract_id}/accounts/{account_id}/orders"
                
        payload = {
            "amount": amount,
            "instrument_id": instrument_id,
            "order_type": 'market',
            "security_id": issuer,
            "side": order_type
        }
        
        return self._session.post(metadata, resource, payload)
    
    
    def getMarketsUSA(self):
        """
        **Get USA Markets. With this method, you can retreive the instrument_id for a given issuer**
        https://api.gbm.com/v1/markets/USA
        
        """
        
        metadata = {
            'tags': ['marketsUSA', 'Trading USA'],
            'operation': 'getMarketsUSA'
        }
        
        resource = "https://api.gbm.com/v1/markets/USA"
        
        return self._session.get(metadata, resource)
    

    def getOrdersUSA(self, account_id):
        """
        **Get orders for the specified Trading USA strategy**
        https://api.trading-usa.gbm.com/v1/orders/contracts/{main_contract_id}/accounts/{account_id}/orders
        
        """
        
        metadata = {
            'tags': ['ordersUSA', 'Trading USA'],
            'operation': 'getOrdersUSA'
        }
        
        main_contract_id = self._session._main_contract_id
        resource = f"https://api.trading-usa.gbm.com/v1/orders/contracts/{main_contract_id}/accounts/{account_id}/orders"
        
        return self._session.get(metadata, resource)
        
        
    