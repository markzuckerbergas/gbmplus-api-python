class Accounts(object):
    def __init__(self, session):
        super(Accounts, self).__init__()
        self._session = session

    def getMainContract(self):
        """
        **Get main contract**
        https://api.gbm.com/v1/contracts
        """

        metadata = {
            'tags': ['dashboard', 'contract', 'account', 'main_contract'],
            'operation': 'getMainContract'
        }

        resource = "https://api.gbm.com/v1/contracts"

        return self._session.get(metadata, resource)[0]


    def getAccounts(self):        
        """
        **List user's accounts (strategies) **
        https://api.gbm.com/v2/contracts/{main_contract}/accounts
        """        

        metadata = {
            'tags': ['dashboard', 'contracts', 'accounts', 'strategies'],
            'operation': 'getAccounts'
        }
        
        resource = f"https://api.gbm.com/v2/contracts/{self._session._main_contract_id}/accounts"

        return self._session.get(metadata, resource)


    def getStrategies(self):
        """
        **Get user's strategies **
        https://api.gbm.com/v2/contracts/{main_contract}/accounts
        """
        return self.getAccounts()
    
    
    def getAccount(self, strategy_name):
        """
        **Get user account by name **        
        """
        accounts = self.getAccounts()
        accounts_dict = {element["name"]: element for element in accounts}

        return accounts_dict.get(strategy_name)
    
    
    def getStrategy(self, strategy_name):
        return self.getAccount(strategy_name)

    
    def getCashTransactions(self, account_id, page=None, page_size=None):
        """
        **Get Cash Transactions for a given account **        
        https://api.gbm.com/v1/contracts/{main_contract}/accounts/{account_id}/cash-transactions?page={page}&page_size={page_size}

        - account_id (string): (required)
        - page (int): (optional)
        - page_size (int): (optional)
        """

        metadata = {
            'tags': ['cash', 'cash transactions', 'accounts'],
            'operation': 'getCashTransactions'
        }

        main_contract_id = self._session._main_contract_id

        if page and page_size:
            resource = f"https://api.gbm.com/v1/contracts/{main_contract_id}/accounts/{account_id}/cash-transactions?page={page}&page_size={page_size}"
        else:
            resource = f"https://api.gbm.com/v1/contracts/{main_contract_id}/accounts/{account_id}/cash-transactions"

        return self._session.get(metadata, resource)

    
    def getStateOfTransfer(self, account_id, transfer_id):
        """
        **Get Transfer state for a given transfer_id **                
        - account_id (string): (required)
        - transfer_id (string): (required)        
        """
        cash_transactions = self.getCashTransactions(account_id)
        transactions_array = cash_transactions.get('items')

        for transaction in transactions_array:
            if transaction.get('transfer_id') == transfer_id:
                return transaction

    
    def getContractBuyingPower(self, legacy_contract_id):
        """
        **Get Buying Power for a given transfer_id **                
        https://homebroker-api.gbm.com/GBMP/api/Operation/GetContractBuyingPower

        - legacy_contract_id (string): (required)
        """        
        
        metadata = {
            'tags': ['buying power', 'contract'],
            'operation': 'getContractBuyingPower'
        }

        resource = "https://homebroker-api.gbm.com/GBMP/api/Operation/GetContractBuyingPower"
        
        payload = {'request': legacy_contract_id}

        return self._session.post(metadata, resource, payload)
    
    
    def getPositionSummary(self, legacy_contract_id):
        """
        **Get the Position Summary for a given legacy_contract_id **                
        https://homebroker-api.gbm.com/GBMP/api/Portfolio/GetPositionSummary

        - legacy_contract_id (string): (required)
        """ 
        
        metadata = {
            'tags': ['position summary', 'position'],
            'operation': 'getPositionSummary'
        }

        resource = "https://homebroker-api.gbm.com/GBMP/api/Portfolio/GetPositionSummary"
        
        payload = {'request': legacy_contract_id}

        return self._session.post(metadata, resource, payload)