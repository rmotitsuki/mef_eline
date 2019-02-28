"""
Module to test the napp kytos/mef_eline.

Add mef_eline source from the installed directory.
"""
import sys
import os
from pathlib import Path as PathLib

if 'VIRTUAL_ENV' in os.environ:
    BASE_ENV = PathLib(os.environ['VIRTUAL_ENV'])
else:
    BASE_ENV = PathLib('/')

MEF_ELINE_PATH = BASE_ENV / 'var/lib/kytos/napps/..'

sys.path.insert(0, str(MEF_ELINE_PATH))
