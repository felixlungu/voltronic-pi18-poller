# PI18 get functions: query and set

from datetime import datetime
from pi18codec import enc, dec
from pi18util import it, tb, snb, isb, sb, f10sb, f1ksb
import asyncio

from aioserial import AioSerial as S

############
### internal utility functions
# PI18 query message from list
def mp(m): return enc(['P'] + m)

# serial write message, read, decode and convert a reply 
async def swrd(s: S, m: bytes, d={'value': lambda x: x}):
    # s.reset_input_buffer()
    # s.reset_output_buffer()
    print(f'SWRD: PORT: {s.port} m: {m}')
    await s.write_async(m)
    b = await s.read_until_async(expected = b'\r')
    print(f'SWRD: port: {s.port} b: {b}')
    r = dec(b)
    if r[0] != 'D': return {'result': r[1]}
    return {'result': 'D'} | dict(map(lambda k,f,x: (k, f(x)), d.keys(), d.values(), r[1:]))


##############
### api functions
# global static strings: don't encode for things that do not change

# PI: get protocol information
_pi = mp(['PI'])
async def pi(s: S): return await swrd(s, _pi, {'version': it})

# T: get device time
_t = mp(['T'])
async def t(s: S): return await swrd(s, _t, {'datetime': tb}) 

# ET: total energy since reset in kWh
dnrg = {'energy': f1ksb}
_et = mp(['ET'])
async def et(s: S): return await swrd(s, _et, dnrg)

# EYyyyy: energy for year 'yyyy' in kWh
# y: int (2022)
async def ey(s: S, y: int):
    _ey = mp(['EY', f'{y:04d}'])
    return await swrd(s, _ey, dnrg)

# EMyyyymm: energy for a year 'yyyy' and month 'mm' in kWh
# y: year int (2022), m: month int (1 for january)
async def em(s: S, y: int, m: int): 
    _em = mp(['EM',f'{y:04d}{m:02d}'])
    return await swrd(s, _em, dnrg)

# EDyyyymmdd: energy for year 'yyyy', month 'mm' and day 'dd'
# y: year, m: month, d: day (1 is first day of the month)
async def ed(s: S, y: int, m: int, d: int): 
    _ed = mp(['EM',f'{y:04d}{m:02d}{d:02d}'])
    return await swrd(s, _ed, dnrg)

# ID: get device serial number
_id = mp(['ID'])
async def id(s: S): return await swrd(s, _id, {'serial number': snb})

# VFW: firmware version
_vfw = mp(['VFW'])
async def vfw(s: S): return await swrd(s, _vfw, {'main cpu version':    sb, 
                                      'slave 1 cpu version': sb,
                                      'slave 2 cpu version': sb})

# _piri = mp(['PIRI'])
# _piri_df = {''}
# def piri(s: S):
