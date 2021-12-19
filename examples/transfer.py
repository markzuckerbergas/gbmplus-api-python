import gbmplus
from datetime import datetime

# Transfer from the Smart Cash strategy to a target strategy

def main():    
    gbm = gbmplus.GBMPlusAPI(output_log=False)

    accounts = gbm.accounts.getAccounts()
    accounts_dict = {element["name"]: element for element in accounts}

    smart_cash_account = accounts_dict.get('Smart Cash')
    target_account = accounts_dict.get('NAME OF YOUR STRATEGY')

    if smart_cash_account and target_account:    
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