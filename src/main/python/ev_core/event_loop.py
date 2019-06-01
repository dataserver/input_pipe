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

from test_utils.sourceDevicesMock import SourceDevicesMock
from ev_core.targetdevices import TargetDevices
from ev_core.eventtree import EventTree
from ev_core.config import Config
import asyncio
from evdev import ecodes
from evdev.events import KeyEvent, AbsEvent, RelEvent
from utils.langutils import *


#
# the central controller pipe which reacts on events from their source devices
# and maps them into proper events in the target devices
# this is sort of the central controller, which controls
# code based on
# https://python-evdev.readthedocs.io/en/latest/tutorial.html#reading-events-from-multiple-devices-using-asyncio
#
class EventController:

    def __init__(self, config: Config):
        self.source_devices = SourceDevicesMock(config)
        self.target_devices = TargetDevices(config)
        self.event_tree = EventTree(config, self.source_devices, self.target_devices)

        for src_dev in self.source_devices.devices:
            asyncio.ensure_future(self.handle_events(src_dev))

        loop = asyncio.get_event_loop()
        loop.run_forever()

    def handle_events(self, src_dev):
        async for event in src_dev.async_read_loop():
            self.resolve_event(event)

    def resolve_event(self, event):
        root_type = self.map_type(event)
        target_rules = save_fetch(lambda: self.event_tree.tree[root_type][event.code], {})

        for key in target_rules:
            target_code, target_device, target_type, target_value = self.get_target_data(event, key, target_rules)
            target_device.write(ecodes.__getattribute__(target_type), target_code, target_value)

    @staticmethod
    def get_target_data(event, key, target_rules):
        target_event = target_rules[key]
        target_type = target_event["ev_type"]
        target_code = target_event["ev_code"]
        target_value = event.value
        target_device = target_event["driver"]
        return target_code, target_device, target_type, target_value

    @staticmethod
    def map_type(event):
        root_type = None
        if isinstance(event, KeyEvent):
            root_type = "EV_KEY"
        elif isinstance(event, AbsEvent):
            root_type = "EV_ABS"
        elif isinstance(event, RelEvent):
            root_type = "EV_REL"

        return root_type
