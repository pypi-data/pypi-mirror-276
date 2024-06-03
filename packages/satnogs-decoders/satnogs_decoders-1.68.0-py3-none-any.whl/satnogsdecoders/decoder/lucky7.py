# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Lucky7(KaitaiStruct):
    """:field obc_id: obc_id
    :field mission_counter: mission_counter
    :field total_reset_counter: total_reset_counter
    :field swap_reset_counter: swap_reset_counter
    :field battery_voltage: battery_voltage
    :field mcu_temperature: mcu_temperature
    :field pa_temperature: pa_temperature
    :field processor_current: processor_current
    :field mcu_voltage_3v3: mcu_voltage_3v3
    :field mcu_voltage_1v2: mcu_voltage_1v2
    :field angular_rate_x_axis: angular_rate_x_axis
    :field angular_rate_y_axis: angular_rate_y_axis
    :field angular_rate_z_axis: angular_rate_z_axis
    :field antenna_burnwire: antenna_burnwire
    """

    class GyroOff(Enum):
        gyro_off = 2001

    class Burnwire(Enum):
        disabled = 0
        enabled = 1

    class ObcId(Enum):
        nominal = 0
        redundant = 128
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.obc_id = KaitaiStream.resolve_enum(Lucky7.ObcId, self._io.read_s2le())
        self.mission_counter = self._io.read_s4be()
        self.callsign_and_satellite_name = (self._io.read_bytes(12)).decode(u"ASCII")
        if not self.callsign_and_satellite_name == u"OK0SATLUCKY7":
            raise kaitaistruct.ValidationNotEqualError(u"OK0SATLUCKY7", self.callsign_and_satellite_name, self._io, u"/seq/2")
        self.total_reset_counter = self._io.read_s2be()
        self.swap_reset_counter = self._io.read_s2be()
        self.battery_voltage = self._io.read_s1()
        self.mcu_temperature = self._io.read_s1()
        self.pa_temperature = self._io.read_s1()
        self.processor_current = self._io.read_u1()
        self.mcu_voltage_3v3 = self._io.read_u1()
        self.mcu_voltage_1v2 = self._io.read_u1()
        self.angular_rate_x_axis = KaitaiStream.resolve_enum(Lucky7.GyroOff, self._io.read_s2be())
        self.angular_rate_y_axis = KaitaiStream.resolve_enum(Lucky7.GyroOff, self._io.read_s2be())
        self.angular_rate_z_axis = KaitaiStream.resolve_enum(Lucky7.GyroOff, self._io.read_s2be())
        self.antenna_burnwire = KaitaiStream.resolve_enum(Lucky7.Burnwire, self._io.read_u1())


