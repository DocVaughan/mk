#!/usr/bin/python
#
# from https://gist.github.com/strahlex/3eaa42f79f7a19e2244a
#

import subprocess
import shlex
import sys
import argparse

if sys.version_info[0] > 2:
    user_input = input
else:
    user_input = raw_input


parser = argparse.ArgumentParser(description='Helper script that register/unregisters simple systemd services')
#parser.add_argument('-n', '--name', help='Name of the machine', default="Machinekit")
parser.add_argument('-u', '--unregister', help='Unregister the service', action='store_true')
parser.add_argument('-d', '--debug', help='Enable debug mode', action='store_true')

args = parser.parse_args()

unregister = args.unregister
debug = args.debug

defaultName = 'mklauncher'
name = user_input('Please enter the name for the service (default: "%s")\n' % defaultName)
if name == '':
    name = defaultName
f = open('/etc/systemd/system/%s.service' % name, 'w')
defaultDescription = 'Mklauncher service'
description = user_input('Please enter a description for the service (default: "%s")\n' % defaultDescription)
if description == '':
    description = defaultDescription
defaultTargets = 'syslog.target network.target'
targets = user_input('After which target should the service start? (default: "%s")\n' % defaultTargets)
if targets == '':
    targets = defaultTargets
defaultUser = 'machinekit'
user = user_input('Which user should start the service? (default: "%s")\n' % defaultUser)
if user == '':
    user = defaultUser
defaultCmd = 'mklauncher /home/machinekit/'
cmd = user_input('Please enter the command that should be started (default: "%s")\n' % defaultCmd)
if cmd == '':
    cmd = defaultCmd

f.write('[Unit]\n'
        'Description=%s\n'
        'After=%s\n'
        '[Service]\n'
        'Type=simple\n'
        'ExecStart=%s\n'
        'User=%s\n'
        '[Install]\n'
        'WantedBy=multi-user.target\n'
        % (description, targets, cmd, user))
f.close()

subprocess.check_call(shlex.split('systemctl daemon-reload'))
subprocess.check_call(shlex.split('systemctl enable %s.service' % name))
