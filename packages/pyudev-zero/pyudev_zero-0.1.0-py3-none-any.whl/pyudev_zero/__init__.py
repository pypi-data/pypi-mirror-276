import os
from typing import Dict, Optional, List, TypeVar, Callable, Literal, Union


def read_symlink(syspath: str, name: str) -> Optional[str]:
    path = os.path.join(syspath, name)
    if not os.path.islink(path):
        return None

    link = os.readlink(path)
    return link.split('/')[-1]


UdevDeviceSelf = TypeVar('UdevDeviceSelf', bound='UdevDevice')


class UdevDevice(object):
    def __init__(self):
        self._properties: Dict[str, Optional[str]] = {}
        self._parent: Optional[UdevDeviceSelf] = None

    def __str__(self):
        return f'SYSNAME: {self.sysname}, SYSPATH: {self.syspath}'

    def _set_properties_from_uevent(self, syspath: str) -> bool:
        path = os.path.join(syspath, 'uevent')
        if not os.path.exists(path):
            return False

        with open(path, 'r') as f:
            for line in f.readlines():
                prop, value = line.strip().split('=', 1)
                if prop == 'DEVNAME':
                    value = f'/dev/{value}'
                self._properties.update({prop: value})

        return True

    def _set_properties_from_evdev(self):
        if self.subsystem and self.subsystem != 'input':
            return
        raise NotImplemented

    def _set_properties_from_props(self):
        if self.subsystem is None or self.subsystem == 'drm':
            return
        parent = self.get_parent_with_subsystem_devtype('pci')
        if parent and parent.sysname:
            self._properties.update({'ID_PATH': f'pci-{self.subsystem}'})

    def _get_property(self, prop: str) -> Optional[str]:
        if prop in self._properties:
            return self._properties[prop]
        return None

    def get_parent_filter(self, filter_fn: Callable[[UdevDeviceSelf], bool]):
        parent = self
        while True:
            parent = parent.parent
            if not parent:
                break
            if filter_fn(parent):
                return parent
        return None

    def get_parent_with_subsystem_devtype(self, subsystem: str, devtype: str = None) -> Optional[UdevDeviceSelf]:
        def filter(device: UdevDeviceSelf) -> bool:
            if not device.subsystem:
                return False
            if device.subsystem != subsystem:
                return False
            if not devtype:
                return True
            if device.devtype == devtype:
                return True
            return False

        return self.get_parent_filter(filter)

    @property
    def parent(self) -> Optional[UdevDeviceSelf]:
        if self._parent:
            return self._parent

        path = self.syspath[5:]
        if not path:
            return None

        while self._parent is None:
            pos = path.rfind('/')
            if pos == -1:
                break
            path = path[:pos]
            self._parent = UdevDevice.new_from_syspath(self.syspath[:5] + path)
            if self._parent:
                break

        return self._parent

    @staticmethod
    def new_from_syspath(syspath: str) -> Optional[UdevDeviceSelf]:
        if not syspath:
            return None

        path = os.path.realpath(syspath)
        if not path:
            return None

        device = UdevDevice()
        if not device._set_properties_from_uevent(path):
            return None

        path = os.path.realpath(syspath)
        sysname = path.split('/')[-1]
        driver = read_symlink(path, 'driver')
        subsystem = read_symlink(path, 'subsystem')

        device._properties.update({'SYSPATH': path})
        device._properties.update({'DEVPATH': path[4:]})
        device._properties.update({'SUBSYSTEM': subsystem})
        device._properties.update({'SYSNAME': sysname})
        device._properties.update({'DRIVER': driver})
        for index, char in enumerate(sysname):
            if char.isdigit():
                device._properties.update({'SYSNUM': sysname[index:]})
                break

        return device

    @staticmethod
    def new_from_devnum(_type: Literal['char', 'block'], devnum: int) -> Optional[UdevDeviceSelf]:
        if _type == 'char' or _type == 'block':
            return UdevDevice.new_from_syspath(f'/sys/dev/{_type}/{os.major(devnum)}:{os.minor(devnum)}')
        return None

    @staticmethod
    def new_from_subsystem_sysname(subsystem: str, sysname: str) -> Optional[UdevDeviceSelf]:
        if not subsystem or not sysname:
            return None
        for path in [f'/sys/bus/{subsystem}/devices/{sysname}', '/sys/class/{subsystem}/{sysname}']:
            if os.path.exists(path):
                return UdevDevice.new_from_syspath(path)
        return None

    @staticmethod
    def new_from_uevent(uevent_buffer: Union[List[str], str]) -> Optional[UdevDeviceSelf]:
        device = UdevDevice()
        counter = 0
        lines: List[str] = uevent_buffer
        if isinstance(uevent_buffer, str):
            lines = uevent_buffer.split('\n')

        for line in lines:
            prop, value = line.strip().split('=', 1)
            if prop == 'DEVPATH':
                syspath = f'/sys{value}'
                sysname = syspath.split('/')[-1]
                device._properties.update({'SYSPATH': syspath})
                device._properties.update({'DEVPATH': value})
                device._properties.update({'SYSNAME': sysname})
                for index, char in enumerate(sysname):
                    if char.isdigit():
                        device._properties.update({'SYSNUM': sysname[index:]})
                        break
                counter += 1
            else:
                if prop in ['SUBSYSTEM', 'ACTION', 'SEQNUM']:
                    counter += 1
                if prop == 'DEVNAME':
                    value = f'/dev/{value}'
                device._properties.update({prop: value})

        if counter != 4:
            return None
        device._set_properties_from_props()
        return device

    @staticmethod
    def new_from_device_id(device_id: str) -> Optional[UdevDeviceSelf]:
        raise NotImplemented

    @staticmethod
    def new_from_device_environment(device_id: str) -> Optional[UdevDeviceSelf]:
        raise NotImplemented

    @property
    def properties(self) -> Dict[str, Optional[str]]:
        return self._properties.copy()

    @property
    def subsystem(self) -> Optional[str]:
        return self._get_property('SUBSYSTEM')

    @property
    def devtype(self) -> Optional[str]:
        return self._get_property('DEVTYPE')

    @property
    def driver(self) -> Optional[str]:
        return self._get_property('DRIVER')

    @property
    def syspath(self) -> Optional[str]:
        return self._get_property('SYSPATH')

    @property
    def sysname(self) -> Optional[str]:
        return self._get_property('SYSNAME')

    @property
    def sysnum(self) -> Optional[str]:
        return self._get_property('SYSNUM')

    @property
    def devpath(self) -> Optional[str]:
        return self._get_property('DEVPATH')

    @property
    def devnode(self) -> Optional[str]:
        return self._get_property('DEVNAME')

    @property
    def seqnum(self) -> int:
        num_str = self._get_property('SEQNUM')
        if num_str:
            return int(num_str)
        return 0

    @property
    def devnum(self) -> int:
        major = self._get_property('MAJOR')
        minor = self._get_property('MINOR')
        if not major or not minor:
            return os.makedev(0, 0)
        return os.makedev(int(major), int(minor))

    @property
    def action(self) -> Optional[str]:
        return self._get_property('ACTION')


def scan_devices(path: str, filter_fn: Callable[[UdevDevice], bool] = None) -> List[UdevDevice]:
    sys_paths = [os.path.join(path, p) for p in os.listdir(path)]
    devices = []
    for sys_path in sys_paths:
        device = UdevDevice.new_from_syspath(sys_path)
        if not device:
            continue
        if not filter_fn:
            devices.append(device)
            continue
        if filter_fn(device):
            devices.append(device)
    return devices


def udev_enumerate_scan_devices(filter_fn: Callable[[UdevDevice], bool] = None) -> List[UdevDevice]:
    path = ['/sys/dev/block', '/sys/dev/char']
    devices = []
    for p in path:
        devices += scan_devices(p, filter_fn)

    return devices
