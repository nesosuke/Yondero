import multiprocessing

bind = '0.0.0.0:8080'

# worker process
workers = 2

# logging
accesslog = 'logs/access.log'
errorlog = 'logs/error.log'
loglevel = 'debug'
logconfig = None
