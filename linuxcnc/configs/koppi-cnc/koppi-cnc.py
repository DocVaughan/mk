#!/usr/bin/env python2

import sys
import os
import subprocess
import importlib
from machinekit import launcher
from time import *

launcher.register_exit_handler()
launcher.set_debug_level(5)
os.chdir(os.path.dirname(os.path.realpath(__file__)))

try:
    launcher.check_installation()
    launcher.cleanup_session()
    launcher.start_process("configserver ~/Machineface ~/Cetus/")
    launcher.start_process('linuxcnc koppi-cnc.ini')
    #launcher.start_process('linuxcnc -v -d koppi-cnc.ini')
except subprocess.CalledProcessError:
    launcher.end_session()
    sys.exit(1)

while True:
    sleep(1)
    launcher.check_processes()
