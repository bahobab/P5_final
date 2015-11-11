#!/usr/bin/python

#import os
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/catalog/")

from catalog import app as application
#s_key = os.urandom(24)
application.secret_key = '\x97\x97&i\x1a\xa36\xbe\x91\xdd\xa6\x01\x88\x18\xfe\xb9\xd9\xbe&\xdeN\x9c-'
