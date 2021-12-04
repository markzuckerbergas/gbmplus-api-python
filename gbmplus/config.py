# Package Constants

# User email, passowrd and client-id, set either at instantiation or as an environment variable 
USER_EMAIL = 'USER_EMAIL'
USER_PASSWORD = 'USER_PASSWORD'
CLIENT_ID = 'CLIENT_ID'

# Maximum number of seconds for each API call
SINGLE_REQUEST_TIMEOUT = 60

# Retry if encountering 4XX errors?
RETRY_4XX_ERROR = False

# 4XX error retry wait time
RETRY_4XX_ERROR_WAIT_TIME = 60

# Retry up to this many times after server-side errors
MAXIMUM_RETRIES = 2

# Create an output log file?
OUTPUT_LOG = True

# Path to output log; by default, working directory of script if not specified
LOG_PATH = ''

# Log file name appended with date and timestamp
LOG_FILE_PREFIX = 'gbmplus_api_'

# Print output logging to console?
PRINT_TO_CONSOLE = True

# Disable all logging? 
SUPPRESS_LOGGING = False