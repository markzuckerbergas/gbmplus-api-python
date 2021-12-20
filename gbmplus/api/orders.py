from datetime import datetime, timezone
from ..exceptions import *

class Orders(object):
    def __init__(self, session, trading_types):
        super(Orders, self).__init__()
        self._session = session
        self._trading_types = trading_types

    def generateOrderObject(self, legacy_contract_id, issuer, quantity, order_type, trading_type, instrument_type, price=None):
        """
        **Generate Order Object**        

        - legacy_contract_id (string): (required)
        - issuer (string): (required)
        - quantity (int): (required)
        - order_type (enum): (required)
        - trading_type (enum): (required)
        - instrument_type (required)
        - price (float): (optional)
        """
        
        if trading_type == self._trading_types.Limited and not price:
            raise OrderFormatError("If trading type is Limited, the price argument is required")
        
        order_object = {
            "algoTradingTypeId": trading_type.value,
            "capitalOrderTypeId": order_type.value,
            "instrumentType": instrument_type.value,
            "issueId": issuer,
            "quantity": quantity,            
            "hash": self.__generateHash(legacy_contract_id, issuer, quantity, instrument_type)
        }
        
        if price:
            order_object["price"] = price
        
        return order_object
    
    def __generateHash(self, legacy_contract_id, issuer, quantity, instrument_type):        
        Now = datetime.now(timezone.utc)
        Now = Now.replace(tzinfo=None)
        Millis = int((Now - datetime(year=1970, day=1, month=1)).total_seconds() * 1000)
        TickerName = issuer.replace(" ", "")
        return f"{str(Millis)}{legacy_contract_id}{TickerName}{str(quantity)}{str(instrument_type.value)}"
    

    def submitOrder(self, legacy_contract_id, duration, order):
        """
        **Submit one order**
        https://homebroker-api.gbm.com/GBMP/api/Operation/RegisterCapitalOrder

        - legacy_contract_id (string): (required)
        - duration (int): (required)             
        - order (object): (required)
        """        
                
        metadata = {
            'tags': ['order', 'generate order'],
            'operation': 'submitOrder'
        }
                
        resource = "https://homebroker-api.gbm.com/GBMP/api/Operation/RegisterCapitalOrder"
        
        payload = {
            "contractId": legacy_contract_id,
            "duration": duration,
            "algoTradingTypeId": order.get("algoTradingTypeId"),
            "orders": [order]
        }

        return self._session.post(metadata, resource, payload)
    
    
    def getOrders(self, legacy_contract_id):
        """
        **Get submitted Orders**
        https://homebroker-api.gbm.com/GBMP/api/Operation/GetBlotterOrders

        - legacy_contract_id (string): (required)        
        """  
        
        metadata = {
            'tags': ['Get Orders'],
            'operation': 'getOrders'
        }
                
        resource = "https://homebroker-api.gbm.com/GBMP/api/Operation/GetBlotterOrders"
        
        payload = {
            "contractId": legacy_contract_id,
            "accountId": legacy_contract_id,
            "instrumentTypes": [0, 2],
            "processDate": datetime.utcnow().strftime('%Y-%m-%dT06:00:00.000Z')
        }
        
        return self._session.post(metadata, resource, payload)
                