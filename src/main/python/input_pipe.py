# MIT License
#
# Copyright (c) 2019 Werner Punz
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# https://python-evdev.readthedocs.io/en/latest/usage.html
import asyncio

from ev_core.config import Config
from ev_core.event_loop import EventController
import argparse
import uvloop
from pidfile import PIDFile

parser = argparse.ArgumentParser(description='Point to the yaml config')

parser.add_argument('--config', "-c",
                    dest='conf',
                    default="./devices.yaml",
                    help='define a config file location (default: ./devices.yaml)')

parser.add_argument('--pidfile', "-p",
                    dest='pidfile',
                    default="/tmp/input_pipe.pid",
                    help='define a pid file location (default: /tmp/input_pipe.pid')


parser.add_argument('--remotekey', "-r",
                    dest='remote_key',
                    default="input_pipe",
                    help='remote key for remote control functions, change only, ' +
                         'if you run multiple instances (default: input_pipe)')

args = parser.parse_args()

uvloop.install()
with PIDFile(args.pidfile):
    EventController(Config(args.conf))

    asyncio.get_event_loop().run_forever()
