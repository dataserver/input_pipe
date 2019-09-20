from test_utils.udevlistener import UdevListener
from test_utils.eventControllerMock import EventControllerMock
from test_utils.udevDeviceMock import UdevDeviceMock


# Listener mock which isolates the system dependend parts
# of the udev and frees the non system dependent ones for testing
class UdevListenerMock(UdevListener):

    def __init__(self, ev_ctl: EventControllerMock):
        self.ev_ctl = ev_ctl
        self.config = ev_ctl.config
        self.restarting = False

    def trigger_event_usb(self, action, device: UdevDeviceMock):
        self._usb_event_handler(action, device)

    def trigger_event_input(self, action, device: UdevDeviceMock):
        self._input_event_handler(action, device)


