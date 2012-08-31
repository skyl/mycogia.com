#!/usr/bin/env python
import sys

from os.path import abspath, dirname, join

from django.conf import settings
from django.core.management import setup_environ, execute_from_command_line

import settings as settings_mod # Assumed to be in the same directory.

setup_environ(settings_mod)
sys.path.insert(0, join(settings.PINAX_ROOT, "apps"))
sys.path.insert(0, join(settings.PROJECT_ROOT, "apps"))

if __name__ == "__main__":
    execute_from_command_line(sys.argv)

