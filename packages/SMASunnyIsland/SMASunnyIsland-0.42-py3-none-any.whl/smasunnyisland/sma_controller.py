#!/usr/bin/env python

"""
SMA_SunnyIslandController: Reading out and controlling a SMA Sunny Island 8.0-13 (battery storage)

MIT License

Copyright (c) 2024 Harm van den Brink

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

__author__ = "Harm van den Brink"
__email__ = "harmvandenbrink@gmail.com"
__license__ = "MIT License"

__version__ = "1.42"
__status__ = "Production"

from vendor.pysunspec.sunspec.core import client as clientSunspec
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from collections import OrderedDict


class SMASunnyIslandClient:
    activate_control_address = 40151
    change_power_address = 40149

    def __init__(
        self,
        modbus_ip,
        modbus_port=502,
        modbus_unit_id=3,
        max_charge_value=-2000,
        max_discharge_value=2000,
    ):
        self.modbus_ip = modbus_ip
        self.modbus_port = modbus_port
        self.modbus_unit_id = modbus_unit_id
        self.max_charge_value = max_charge_value
        self.max_discharge_value = max_discharge_value
        self.modbus_client = ModbusClient(
            modbus_ip,
            port=modbus_port,
            unit_id=modbus_unit_id,
            auto_open=True,
            auto_close=True,
        )
        self.sunSpecClient = clientSunspec.SunSpecClientDevice(
            clientSunspec.TCP, 126, ipaddr=modbus_ip, ipport=modbus_port, timeout=2.0
        )
        pass

    def read_sma_values(self):
        self.sunSpecClient.common.read()
        self.sunSpecClient.nameplate.read()
        self.sunSpecClient.status.read()
        self.sunSpecClient.controls.read()
        self.sunSpecClient.inverter.read()
        self.sunSpecClient.storage.read()

        sma = OrderedDict(
            [
                ("Mn", self.sunSpecClient.common.Mn),
                ("Md", self.sunSpecClient.common.Md),
                ("Opt", self.sunSpecClient.common.Opt),
                ("Vr", self.sunSpecClient.common.Vr),
                ("SN", self.sunSpecClient.common.SN),
                ("DERTyp", self.sunSpecClient.nameplate.DERTyp),
                ("WRtg", self.sunSpecClient.nameplate.WRtg),
                ("WHRtg", self.sunSpecClient.nameplate.WHRtg),
                ("AhrRtg", self.sunSpecClient.nameplate.AhrRtg),
                ("MaxChaRte", self.sunSpecClient.nameplate.MaxChaRte),
                ("MaxDisChaRte", self.sunSpecClient.nameplate.MaxDisChaRte),
                ("PVConn", self.sunSpecClient.status.PVConn),
                ("StorConn", self.sunSpecClient.status.StorConn),
                ("ECPConn", self.sunSpecClient.status.ECPConn),
                ("ActWh", self.sunSpecClient.status.ActWh),
                ("WMaxLimPct", self.sunSpecClient.controls.WMaxLimPct),
                ("WMaxLim_Ena", self.sunSpecClient.controls.WMaxLim_Ena),
                ("OutPFSet_Ena", self.sunSpecClient.controls.OutPFSet_Ena),
                ("VArPct_Mod", self.sunSpecClient.controls.VArPct_Mod),
                ("VArPct_Ena", self.sunSpecClient.controls.VArPct_Ena),
                ("AphA", self.sunSpecClient.inverter.AphA),
                ("AphB", self.sunSpecClient.inverter.AphB),
                ("AphC", self.sunSpecClient.inverter.AphC),
                ("PhVphA", self.sunSpecClient.inverter.PhVphA),
                ("PhVphB", self.sunSpecClient.inverter.PhVphB),
                ("W", self.sunSpecClient.inverter.W),
                ("Hz", self.sunSpecClient.inverter.Hz),
                ("VAr", self.sunSpecClient.inverter.VAr),
                ("WH", self.sunSpecClient.inverter.WH),
                ("Evt1", self.sunSpecClient.inverter.Evt1),
                ("WChaMax", self.sunSpecClient.storage.WChaMax),
                ("StorCtl_Mod", self.sunSpecClient.storage.StorCtl_Mod),
                ("ChaState", self.sunSpecClient.storage.ChaState),
                ("InBatV", self.sunSpecClient.storage.InBatV),
                ("ChaSt", self.sunSpecClient.storage.ChaSt),
            ]
        )
        return sma

    def limit_power(self, num, minimum, maximum):
        return int(max(min(num, maximum), minimum))

    def send_modbus(self, address, value, type):
        if self.modbus_client.connect() == False:
            print("Modbus connection lost, trying to reconnect...")
            print("Modbus Connected: {}".format(self.modbus_client.connect()))
        else:
            # SMA expects everything in Big Endian format
            builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
            # Only unsigned int32 and signed int32 are built in. It is enough to control the flow of power of the battery.
            if type == "uint32":
                builder.add_32bit_uint(value)
            if type == "int32":
                builder.add_32bit_int(value)
            registers = builder.to_registers()
            self.modbus_client.write_registers(address, registers, unit=3)

    def set_power_setpoint(self, power):
        # 40149 Active power setpoint - int32
        # 40151 Eff./reac. pow. contr. via comm. 802 = "active" 803 = "inactive", ENUM - uint32
        # 40153 Reactive power setpoint - uint32
        # 0x0322 is the value (802) to activate the control of power via modbus communication
        self.send_modbus(self.activate_control_address, 0x0322, "uint32")
        self.send_modbus(
            self.change_power_address,
            self.limit_power(
                power, minimum=self.max_charge_value, maximum=self.max_discharge_value
            ),
            "int32",
        )