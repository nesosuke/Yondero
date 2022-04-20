import multiprocessing

bind = '0.0.0.0:5000'

# worker process
workers = 2

# logging
accesslog = 'logs/access.log'
errorlog = 'logs/error.log'
loglevel = 'debug'
logconfig = None
