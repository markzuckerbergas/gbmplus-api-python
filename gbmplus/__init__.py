from datetime import datetime
from enum import Enum
import logging
import os

from .rest_session import *
from .api.accounts import Accounts
from .api.transfers import Transfers
from .api.orders import Orders
from .api.tradingUSA import TradingUSA

from .config import (
    USER_EMAIL, USER_PASSWORD, CLIENT_ID, SINGLE_REQUEST_TIMEOUT,
    RETRY_4XX_ERROR, RETRY_4XX_ERROR_WAIT_TIME, MAXIMUM_RETRIES,
    OUTPUT_LOG, LOG_PATH, LOG_FILE_PREFIX, PRINT_TO_CONSOLE, SUPPRESS_LOGGING
)

__version__ = '0.12'

class GBMPlusAPI(object):
    """
    **Creates a persistent GBM+ API session**
    - user_email (string): GBM+ User Email
    - user_password (string): GBM+ User Password
    - client_id (string): GBM+ User Client ID
    - single_request_timeout (integer): maximum number of seconds for each API call  
    - retry_4xx_error (boolean): retry if encountering 4XX errors?
    - retry_4xx_error_wait_time (integer): 4XX error retry wait time
    - maximum_retries (integer): retry up to this many times when encountering server-side errors
    - output_log (boolean): create an output log file?
    - log_path (string): path to output log; by default, working directory of script if not specified
    - log_file_prefix (string): log file name appended with date and timestamp
    - print_console (boolean): print logging output to console?
    - suppress_logging (boolean): disable all logging? 
    """

    def __init__(self, user_email=None, user_password=None, client_id=None,
                 single_request_timeout=SINGLE_REQUEST_TIMEOUT, maximum_retries=MAXIMUM_RETRIES,
                 retry_4xx_error= RETRY_4XX_ERROR,retry_4xx_error_wait_time=RETRY_4XX_ERROR_WAIT_TIME,
                 output_log=OUTPUT_LOG, log_path=LOG_PATH, log_file_prefix=LOG_FILE_PREFIX,
                 print_console=PRINT_TO_CONSOLE, suppress_logging=SUPPRESS_LOGGING):
                
        user_email = user_email or os.getenv(USER_EMAIL)        
        user_password = user_password or os.getenv(USER_PASSWORD)
        client_id = client_id or os.getenv(CLIENT_ID)    
        
        if not user_email or not user_password or not client_id:
            raise UserError()

        # Configure logging
        if not suppress_logging:
            self._logger = logging.getLogger(__name__)
            self._logger.setLevel(logging.DEBUG)

            formatter = logging.Formatter(
                fmt='%(asctime)s %(name)12s: %(levelname)8s > %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler_console = logging.StreamHandler()
            handler_console.setFormatter(formatter)

            if output_log:
                if log_path and log_path[-1] != '/':
                    log_path += '/'
                self._log_file = f'{log_path}{log_file_prefix}_log__{datetime.now():%Y-%m-%d_%H-%M-%S}.log'
                handler_log = logging.FileHandler(
                    filename=self._log_file
                )
                handler_log.setFormatter(formatter)

            if output_log and not self._logger.hasHandlers():
                self._logger.addHandler(handler_log)
                if print_console:
                    handler_console.setLevel(logging.INFO)
                    self._logger.addHandler(handler_console)
            elif print_console and not self._logger.hasHandlers():
                self._logger.addHandler(handler_console)
        else:
            self._logger = None

        # Creates the API session
        self._session = RestSession(
            logger=self._logger,
            user_email=user_email,
            user_password=user_password,
            client_id=client_id,
            single_request_timeout=single_request_timeout,
            retry_4xx_error=retry_4xx_error,
            retry_4xx_error_wait_time=retry_4xx_error_wait_time,
            maximum_retries=maximum_retries
        )        

        # Authenticate User
        self._session.authenticate()

        # Get Main Contract ID
        self._session.getMainContract()

        # API endpoints by section
        self.accounts = Accounts(self._session) 
        self.transfers = Transfers(self._session)
        self.orders = Orders(self._session, trading_types=TradingTypes)
        self.tradingUSA = TradingUSA(self._session)


class OrderTypes(Enum):
    Buy = 1
    Sell = 8
    
class TradingTypes(Enum):
    Limited = 0
    Market = 5    
    
class InstrumentTypes(Enum):
    SIC = 0
    IPC = 2