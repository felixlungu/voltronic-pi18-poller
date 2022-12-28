# PI18 get functions: query and set

from datetime import datetime
from pi18codec import enc, dec
from pi18util import it, tb, snb, isb, sb, f10sb, f1ksb

from serial import Serial as S

############
### internal utility functions
# PI18 query message from list
def mp(m): return enc(['P'] + m)

# serial write message, read, decode and convert a reply 
def swrd(s: S, m: bytes, f=[it]):
    s.reset_input_buffer()
    s.reset_output_buffer()
    print('SWRD: m: ',m, '\n')
    s.write(m)
    s.flush()
    b = s.read_until(expected = b'\r')
    print('SWRD b: ', b, '\n')
    return dec(b)

# convert the results from swrd
def swrdf(s: S, m: bytes, f=[lambda x: x]):
    r = swrd(s, m)
    if r[0] != 'D': return ''
    return list(map(lambda f,x: f(x), f,r[1:]))


##############
### api functions
# global static strings: don't encode for things that do not change

# PI: get protocol information
_pi = mp(['PI'])
def pi(s: S): return swrdf(s, _pi)

# T: get device time
_t = mp(['T'])
def t(s: S): return swrdf(s, _t, [tb]) 

# ET: total energy since reset in Wh
_et = mp(['ET'])
def et(s: S): return swrdf(s, _et, [f1ksb])

# EYyyyy: energy for year 'yyyy' in Wh
# y: int (2022)
def ey(s: S, y: int):
    _ey = mp(['EY', f'{y:04d}'])
    return swrdf(s, _ey, [f1ksb])

# EMyyyymm: energy for a year 'yyyy' and month 'mm' in Wh
# y: year int (2022), m: month int (1 for january)
def em(s: S, y: int, m: int): 
    _em = mp(['EM',f'{y:04d}{m:02d}'])
    return swrdf(s, _em, [f1ksb])

# EDyyyymmdd: energy for year 'yyyy', month 'mm' and day 'dd'
# y: year, m: month, d: day (1 is first day of the month)
def ed(s: S, y: int, m: int, d: int): 
    _ed = mp(['EM',f'{y:04d}{m:02d}{d:02d}'])
    return swrdf(s, _ed, [f1ksb])

# ID: get device serial number
_id = mp(['ID'])
def id(s: S): return swrdf(s, _id, [snb])

# VFW: firmware version
_vfw = mp(['VFW'])
def vfw(s: S): return swrdf(s, _vfw, [sb, sb, sb])

