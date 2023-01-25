# PI18 get/query functions

from dataclasses import dataclass
from aioserial import AioSerial as S
from datetime import date
import pi18d as D
import pi18m as M
import pi18c as C


##############
### api functions
class PI18:
    port: str
    ser: S = None
    pi: str = None
    id: str = None
    vfw: str = None
    # gs: dict = dict() # last status

    def __init__(self, port: str = '/dev/ttyUSB0', timeout = None):
        self.ser = S(port, 2400, timeout=timeout)
    
    # @classmethod
    # async def init(cls, port: str):
    #     ser = R.AioSerial(port, 2400)
    #     pi = (await G.pi(ser))[1][0]
    #     id = (await G.id(ser))[1][0]
    #     vfw = (await G.vfw(ser))[1][0]
    #     return cls(ser, pi, id, vfw)

    # PI: get protocol information
    async def pi(self): return await C.drws(self.ser, M.pi)
    
    # T: get device time
    async def t(self): return await C.drws(self.ser, M.t) 
    
    # ET: total energy since reset in kWh
    async def et(self): return await C.drws(self.ser, M.e, D.mp(['ET']))
    
    # EYyyyy: energy for year 'yyyy' in kWh
    # y: int (2022)
    async def ey(self, y: int = None): 
        td = date.today()
        if y == None: y = td.year
        return await C.drws(self.ser, M.e, D.mp(['EY', f'{y:04d}']))
    
    # EMyyyymm: energy for a year 'yyyy' and month 'mm' in kWh
    # y: year int (2022), m: month int (1 for january)
    async def em(self, y: int = None, m: int = None): 
        td = date.today()
        if y == None: y = td.year
        if m == None: m = td.month
        return await C.drws(self.ser, M.e, D.mp(['EM',f'{y:04d}{m:02d}']))
    
    # EDyyyymmdd: energy for year 'yyyy', month 'mm' and day 'dd'
    # y: year, m: month, d: day (1 is first day of the month)
    async def ed(self, y: int = None, m: int = None, d: int = None):
        td = date.today()
        if y == None: y = td.year
        if m == None: m = td.month
        if d == None: d = td.day
        return await C.drws(self.ser, M.e, D.mp(['EM',f'{y:04d}{m:02d}{d:02d}']))
    
    # ID: get device serial number
    async def id(self): return await C.drws(self.ser, M.id)
    
    # VFW: firmware version
    async def vfw(self): return await C.drws(self.ser, M.vfw)
    
    # PIRI: get the device rated information
    # _piri = mp(['PIRI'])
    # async def piri(s: S):
    
    # GS: get current status of the device
    async def gs(self): return await C.drws(self.ser, M.gs)
    

if __name__ == "__main__":
    import asyncio as A
    # ports = ['/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyUSB2', '/dev/ttyUSB3', '/dev/ttyUSB4', '/dev/ttyUSB5']
    ports = ['/dev/ttyUSB1', '/dev/ttyUSB2', '/dev/ttyUSB3', '/dev/ttyUSB4', '/dev/ttyUSB5']
    inv = [PI18(x, 1) for x in ports]
    async def doit(x): return await A.gather(*x)

    def dprint(h, x):
        print(h)
        for m in x: print(m[1])
        return
    
    dprint(M.pi.names, A.run(doit([x.pi() for x in inv])))
    dprint(M.t.names, A.run(doit([x.t() for x in inv])))
    dprint(M.e.names, A.run(doit([x.et() for x in inv])))
    dprint(M.e.names, A.run(doit([x.ey() for x in inv])))
    dprint(M.e.names, A.run(doit([x.em() for x in inv])))
    dprint(M.e.names, A.run(doit([x.ed() for x in inv])))
    dprint(M.id.names, A.run(doit([x.id() for x in inv])))
    dprint(M.vfw.names, A.run(doit([x.vfw() for x in inv])))
    dprint(M.gs.names, A.run(doit([x.gs() for x in inv])))
