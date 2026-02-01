import os

# Colors
ENDC = "\033[0m"
WARNING = "\033[93m"
OKGREEN = "\033[92m"
OKCYAN = "\033[96m"
FAIL = "\033[91m"

DEBUG = bool(int(os.getenv("DEBUG", 0)))

if DEBUG:
    from config.settings.test import *  # noqa
else:
    from config.settings.production import *  # noqa

print(OKCYAN + "-- Production settings imported --" + ENDC)

if DEBUG:
    mode = FAIL + "ON" + ENDC
else:
    mode = OKCYAN + "OFF" + ENDC

print(OKCYAN + "-- Debug mode is: " + mode + OKCYAN + " --" + ENDC)
