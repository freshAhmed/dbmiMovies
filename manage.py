#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import dotenv
import logging
import pathlib
logging.basicConfig(level=logging.DEBUG,format=' %(filename)s- %(asctime)s - %(levelname)s - %(message)s')

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dbmi.settings')
    try:
        dotenv_File_path=pathlib.Path() / '.env'
        if dotenv_File_path.exists() :
         dotenv.read_dotenv()
        else:
          raise FileNotFoundError("i can't finde dot env file !!")
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
