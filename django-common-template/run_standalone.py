#!/usr/bin/env python
import sys
from django.core.management import setup_environ
import imp
try:
    imp.find_module('settings') # Assumed to be in the same directory.
except ImportError:
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n" % __file__)
    sys.exit(1)

import settings

setup_environ(settings)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        mod = sys.argv[1]
        try:
            mod_obj = __import__("cardea.standalone.%s"%mod, fromlist=["cardea.standalone"])
        except ImportError, e:
            sys.stderr.write("Cannot find standalone module [%s].\n"%mod)
            sys.exit(1)