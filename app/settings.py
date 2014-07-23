
# The URL to the Broker used for Celery
CELERY_BROKER_URL='amqp://guest@localhost//'

# The backend messaging system for Celery.  Most
# likely the same as the BROKER_URL
CELERY_RESULT_BACKEND='amqp://guest@localhost//'

# The key used to authenitcate against the 
# Weather Underground API
WUNDERGROUND_KEY='6aae3b03b1f8a450'
LISTEN_ADDRESS='0.0.0.0'
LISTEN_PORT=5000

CALLBACK_IP='127.0.0.1'
CALLBACK_PORT=5000