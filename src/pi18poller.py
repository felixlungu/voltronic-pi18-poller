import asyncio
from dataclasses import dataclass
import aioserial as R
import pi18get as G

# try to send a second time if the inverter throws a 'NAK' response
# it can happen if there is a longer pause between requests
async def try2(f,a):
    r = await f(*a)
    if r['result'] != 'NAK': return r
    return await f(*a)

@dataclass
class PI18:
    port: str
    ser: R.aioserial
    pi: str
    id: str
    vfw: dict

    @classmethod
    async def init(cls, port: str):
        ser = R.AioSerial(port, 2400)
        pi = (await try2(G.pi, [ser]))['version']
        id = (await try2(G.id, [ser]))['serial number']
        vfw = await try2(G.vfw, [ser]) 
        return cls(port, ser, pi, id, vfw)


dev = ['/dev/ttyUSB1', '/dev/ttyUSB2', '/dev/ttyUSB3', '/dev/ttyUSB4', '/dev/ttyUSB5']

async def main():
    tsks = set()
    inv = dict()

    def icb(tsk: asyncio.Task):
        r: PI18 = tsk.result()
        inv[r.id] = r
        tsks.discard(tsk)


    try:
        async with asyncio.TaskGroup() as tg:
            for x in dev:
                tsk = tg.create_task(PI18.init(x))
                tsks.add(tsk)
                tsk.add_done_callback(icb)

    except* Exception as eg:
        for e in eg.exceptions:
            print(e)
    
    # print(f'inv: {inv}')

    

asyncio.run(main())

# loop = asyncio.get_event_loop()
# print(loop.run_until_complete(asyncio.gather(*[PI18.create(x) for x in dev], return_exceptions=False)))

# print(invert)

# loop = asyncio.get_event_loop()
# inv = loop.run_until_complete(asyncio.gather(PI18(x) for x in dev))

# print(inv)

# D = list(aioserial.AioSerial(d, 2400) for d in dev)
# print(f"D:{D}")

# pi = P.pi(s)

# print('PI', pi)

# pi = P.pi(s)

# print('PI', pi)

# pi = P.pi(s)

# print('PI', pi)

# id = P.id(s)
# print('ID: ', id)


# t = P.t(s)
# print('T: ', t)
# et = P.et(s)
# print('ET: ', et)
