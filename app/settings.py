
# The URL to the Broker used for Celery
CELERY_BROKER_URL='amqp://guest@localhost//'

# The backend messaging system for Celery.  Most
# likely the same as the BROKER_URL
CELERY_RESULT_BACKEND='amqp://guest@localhost//'

# The key used to authenitcate against the 
# Weather Underground API
WUNDERGROUND_KEY='6aae3b03b1f8a450'

# The IP Address that Flask will bind to
LISTEN_ADDRESS='0.0.0.0'

# The port that Flask will listen on for 
#connections
LISTEN_PORT=5000

# This IP Address is used to build the callback 
# URL that you use to get your celery results
CALLBACK_IP='127.0.0.1'

# This is the port that is used to build the 
# callback URL for the celery results
CALLBACK_PORT=5000