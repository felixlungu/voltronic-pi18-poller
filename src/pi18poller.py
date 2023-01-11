import asyncio as A
from dataclasses import dataclass
import aioserial as R
import pi18 as G
import pi18m as M

@dataclass
class PI18:
    ser: R.aioserial
    pi: str
    id: str
    vfw: dict
    # gs: dict = dict() # last status

    @classmethod
    async def init(cls, port: str):
        ser = R.AioSerial(port, 2400)
        pi = (await G.pi(ser))[1][0]
        id = (await G.id(ser))[1][0]
        vfw = (await G.vfw(ser))[1][0]
        return cls(ser, pi, id, vfw)


dev = ['/dev/ttyUSB1', '/dev/ttyUSB2', '/dev/ttyUSB3', '/dev/ttyUSB4', '/dev/ttyUSB5']
inv = dict()

async def init(d):
    r = await A.gather(*[PI18.init(x) for x in d])
    return  dict(zip([x.id[0] for x in r],r))
    
async def main():
    global inv
    inv = await init(dev)
    print(f'inv: {inv}')
    r = await A.gather(*[G.gs(x.ser) for x in inv.values()])
    for g in r:
        print(g)

A.run(main())