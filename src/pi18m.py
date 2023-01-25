# PI18 message formating and field decoding mapping

import pi18u as U
import pi18d as D
from dataclasses import dataclass

@dataclass(slots=True)
class PI18MSG:
    qmsg: bytes # query msg
    flags: list # decode flags for received field
    funcs: tuple
    names: tuple
    units: tuple

# Decode names, functions and unit for reply messages if the decode flag is True
#   q: encoded query message
#   l: [['name', conv_function(bytes), 'unit', decode?(True|False)], [....]]
#   returns PI18MSG([[booleans for which to decode,...], (functions,...), ('names',...), ('units',...)]
def dfnu(q: bytes, l: list):
    g = [x[3] for x in l]
    f, n, u = zip(*[[x[1], x[0], x[2]] for x in l if x[3]])
    return PI18MSG(q,g,f,n,u)

# default decode
d = dfnu(b'', [['value', (lambda x: x),'', True]])

# PI: get protocol information
pi = dfnu(D.mp(['PI']), [['Version', U.it, '', True]])

# T: get device time
t = dfnu(D.mp(['T']), [['Datetime', U.tb, 'datetime', True]])

# ET, EY, EM, ED:  energy in kWh
e = dfnu(b'', [['Energy', U.f1ksb, 'kWh', True]])

# ID: get device serial number
id = dfnu(D.mp(['ID']), [['Serial number', U.snb, '', True]])

# VFW: firmware version
vfw = dfnu(D.mp(['VFW']), 
           [['main cpu version',    U.sb, '', True],
            ['slave 1 cpu version', U.sb, '', False], 
            ['slave 2 cpu version', U.sb, '', False]])           


# PIRI: get the device rated information
# piri = dfnu([[]])

# GS: get current status of the device
gs = dfnu(D.mp(['GS']), 
           [['AC grid voltage',           U.f10sb, 'V', True],
            ['AC grid frequency',         U.f10sb, 'Hz', True], 
            ['AC output voltage',         U.f10sb, 'V', True],
            ['AC output frequency',       U.f10sb, 'Hz', True], 
            ['AC output apparent power',  U.f1ksb, 'VA', True],
            ['AC output active power',    U.f1ksb, 'kW', True],
            ['AC load',                   U.isb, '%', True],
            ['Battery voltage',           U.f10sb, 'V', True], 
            ['Battery voltage from SCC',  U.f10sb, 'V', False],
            ['Battery voltage from SCC2', U.f10sb, 'V', False],
            ['Battery discharge current', U.isb, 'A', True], 
            ['Battery charging current',  U.isb, 'A', True], 
            ['Battery capacity',          U.isb, '%', False], 
            ['Inverter heat sink temperature', U.isb, 'C', True],
            ['MPPT1 charger temperature', U.isb, 'C', False], 
            ['MPPT2 charger temperature', U.isb, 'C', False],
            ['PV1 Input power',           U.f1ksb, 'kW', True], 
            ['PV2 Input power',           U.f1ksb, 'kW', False],
            ['PV1 Input voltage',         U.f10sb, 'V', True], 
            ['PV2 Input voltage',         U.f10sb, 'V', False], 
            ['Setting value configuration state', U.stsb, '', True],
            ['MPPT1 charger status',      U.chsb, '', True],
            ['MPPT2 charger status',      U.chsb, '', False], 
            ['Load connection',           U.lcsb, '', True], 
            ['Battery power direction',   U.bchsb, '', True], 
            ['DC/AC power direction',     U.dcacsb, '', True],
            ['Line power direction',      U.lpdsb, '', True], 
            ['Local parallel ID',         U.isb, '', True]])
