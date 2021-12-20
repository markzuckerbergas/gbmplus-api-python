import gbmplus
from datetime import datetime

# Transfer money from the Smart Cash strategy to a target strategy

def main():    
    
    # Instantiate trader object
    gbm = gbmplus.GBMPlusAPI(output_log=False)

    # Get all of the accounts (strategies) and place them in a dictionary 
    accounts = gbm.accounts.getAccounts()
    accounts_dict = {element["name"]: element for element in accounts}

    # Get source/origin and target/destination account
    smart_cash_account = accounts_dict.get('Smart Cash')
    target_account = accounts_dict.get('NAME OF YOUR STRATEGY') # Replace with your desired strategy

    if smart_cash_account and target_account:    
        
        # Initiate Transfer for 100 MXN pesos
        response = gbm.transfers.transfer(
            amount=100, # in MXN
            origin_account_id=smart_cash_account.get('account_id'),
            target_account_id=target_account.get('account_id')
        )

        print(response)
        
if __name__ == '__main__':
    start_time = datetime.now()
    main()
    end_time = datetime.now()
    print(f'\nScript complete, total runtime {end_time - start_time}')