# PI18 communication

from aioserial import AioSerial as S
import pi18d as D
import pi18m as M
from itertools import compress
import asyncio as A

# send & receive raw message
async def rwsm(s: S, m: bytes):
    s.flushOutput()
    s.flushInput()
    await s.write_async(m)
    b = await s.read_async(5) # get the preamble "^Dxxx...", "^0cc\r" or '^1cc\r
    if b[1:2] != b'D': return b
    n = int(b[2:5].decode())
    b += await s.read_async(n)
    return b


# serial write message, read, decode and convert a reply 
async def drws(s: S,  c: M.PI18MSG, m: bytes = None):
    if m == None: m = c.qmsg
    b = await rwsm(s, m)
    d = D.dec(b)
    if not d[0] in ['D','1']:
        await rwsm(s, M.pi.qmsg) # for a wakeup with 'PI'
        b = await rwsm(s, m) # retry the initial message
        d = D.dec(b)

    if d[0] !='D': return d
    g = [*compress(d[1:], c.flags)]
    r = [*map(lambda f,x:f(x), c.funcs, g)]
    return ['D', r]
