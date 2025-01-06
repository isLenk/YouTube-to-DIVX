import psutil
import sys
# Import only if running on Linux
try:
    import pyudev
except ImportError:
    pass

# Import only if running on Windows
try:
    import win32file
except ImportError:
    pass

from PyQt6.QtWidgets import QComboBox

def get_usb_drive_info():
    usb_devices = []
    if sys.platform.startswith("linux") and pyudev:
        context = pyudev.Context()
        for device in context.list_devices(subsystem='usb', DEVTYPE='usb_device'):
            usb_devices.append(device.device_node)
            print(device)
    elif sys.platform.startswith("win") and win32com.client:
        wmi = win32com.client.GetObject("winmgmts:")
        for usb in wmi.InstancesOf("Win32_USBHub"):
            usb_devices.append(usb.DeviceID)
    else:
        for device in psutil.disk_partitions():
            if 'usb' in device.opts:
                usb_devices.append(device.device)
    return usb_devices



class USBSelect(QComboBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.populate()

    def populate(self):
        usb_drives = get_usb_drive_info()
        for drive in usb_drives:
            self.addItem(drive)
            # self.addItem(drive['mount_point'])