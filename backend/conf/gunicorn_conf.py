bind = '0.0.0.0:8000'
workers = 5
timeout = 120
certfile = '/home/des/fullchain.pem'
keyfile = '/home/des/privkey.pem'
# Access log - records incoming HTTP requests
#accesslog = "/var/log/gunicorn/gunicorn.access.log"
# Error log - records Gunicorn server goings-on
#errorlog = "/var/log/gunicorn/gunicorn.error.log"
# Whether to send Django output to the error log
#capture_output = True
# How verbose the Gunicorn error logs should be
# loglevel = "info"