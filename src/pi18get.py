# PI18 get functions: query and set

from datetime import datetime
from pi18codec import enc, dec
import serial

############
### internal utility functions
def em(m): return enc(['P'] + m)

# serial write message, read and decode reply 
def swrd(ser, m):
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    ser.write(m)
    ser.flush()
    b = ser.read_until(expected = b'\r')
    return dec(b)


##############
### api functions
# global static strings: don't encode for things that do not change

# PI: get protocol information
_pi = em(['PI'])
def pi(ser):
    m = swrd(ser, _pi)
    if m[0] != 'D': return ''
    return m[1]

# T: get device time
_t = em(['T'])
def t(ser):
    m = swrd(ser, _t)
    if m[0] != 'D': return ''
    return datetime.strptime(m[1], '%Y%m%d%H%M%S')

# ET: total generated energy since reset in Wh
_et = em(['ET'])
def et(ser):
    m = swrd(ser, _et)
    if m[0] != 'D': return ''
    return int(m[1])

# EYyyyy: total energy for year yyyy in Wh
# y: int (2022)
# TODO: use f'04...
def ey(ser, y):
    _ey = em(['EY', y])
    m = swrd(ser, _ey)
    if m[0] != 'D': return ''
    return int(m[1])

# EMyyyymm: total energy for a year yyyy and month mm
# y: year int (2022), m: month int (1 for january)



# ID: get device serial number
_id = em('ID')
def id(ser):
    m = swrd(ser,_id)
    if m[0] != 'D': return ''
    n = int(m[1][0:2])
    return m[1][2:2+n]
    



