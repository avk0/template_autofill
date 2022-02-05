#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/template_autofill/")

import os
print(os.getegid(), os.geteuid())
#print(sys.path)
#sys.path.insert(0, '/home/ubuntu/.local/lib/python3.8/site-packages')

activate_this = '/var/www/template_autofill/env/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

#python_home = '/var/www/template_autofill/env'
#activate_this = python_home + '/bin/activate_this.py'
#exec(activate_this, dict(__file__=activate_this))

from template_autofill import create_app


#if __name__ == "__main__":
application = create_app()
    #app.run()
