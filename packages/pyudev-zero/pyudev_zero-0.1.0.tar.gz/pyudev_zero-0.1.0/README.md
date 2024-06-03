# pyudev-zero
A pure Python implementation of libudev-zero

## Usages
List all devices
```python
import json

for dev in udev_enumerate_scan_devices():
    print(f'Device {dev}: {json.dumps(dev.properties, indent=4)}')
```

List all USB tty devices
```python
import json

for dev in udev_enumerate_scan_devices(lambda d: d.subsystem == 'tty'):
    parent = dev.get_parent_filter(lambda d: d.subsystem == 'usb')
    if parent:
        print(f'Device {dev}: {json.dumps(dev.properties, indent=4)}')
        print(f'Parent {parent}: {json.dumps(parent.properties, indent=4)}')
```

## Not support
Udev netlink monitoring is currently not supported.

## Thanks
This library is rewritten from [libudev-zero](https://github.com/illiliti/libudev-zero).
