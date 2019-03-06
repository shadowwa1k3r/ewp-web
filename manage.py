#!/usr/bin/env python
import os
import sys

prod = True 
if __name__ == '__main__':
    if prod:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ewpadmin.settings')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ewpadmin.devsettings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
