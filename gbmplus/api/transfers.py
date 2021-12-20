class Transfers(object):
    def __init__(self, session):
        super(Transfers, self).__init__()
        self._session = session

    
    def transfer(self, amount, origin_account_id, target_account_id):        
        """
        **Transfer an specific amount from one account to a target account**
        https://api.gbm.com/v1/contracts/{main_contract_id}/accounts/{origin_account_id}/transfers

        - amount (float): Amount in MXN to transfer
        - origin_account_id (string): ID of the origin account
        - target_account_id (string): ID of the target account to transfer
        """        

        kwargs = locals()

        metadata = {
            'tags': ['transfers', 'origin_account', 'target_account'],
            'operation': 'transfer'
        }
        
        main_contract_id = self._session._main_contract_id
        resource = f"https://api.gbm.com/v1/contracts/{main_contract_id}/accounts/{origin_account_id}/transfers"

        body_params = ['amount', 'target_account_id']
        payload = {k.strip(): v for k, v in kwargs.items() if k.strip() in body_params}

        return self._session.post(metadata, resource, payload)