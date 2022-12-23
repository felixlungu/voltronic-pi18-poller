
# vim:set sw=4 ts=4 et

import crcmod
crc=crcmod.predefined.mkPredefinedCrcFun('xmodem')

# encode a PI18 message:
#   m: ['P' or 'S', 'MGSGtype', values...]
# ex: enc(['P','EY','2022']) -> b'^P009EY2022\xe5\x9d\r
def enc(m):
    mt = m[0].encode()
    s = m[1].encode() + ','.join(str(x) for x in m[2:]).encode()
    c = crc(s).to_bytes(2,'big')
    t = s + c + b'\r'
    return b'^' + mt + ('%03d'%len(t)).encode() + t

# decode a PI18 message
# m: b'^D0251401234567890123456789p\xa2\r' -> ['D', '1401234567890123456789']
# first element is either '0' for error, '1' for accepted set msg or 'D' for query reply
def dec(m):
    if m[0:1] != b'^' or m[-1:] != b'\r': return ['0', 'malformed']

    mt = m[1:2].decode()
    if mt == '0': return ['0', 'rejected']   # rejected command: not implemented or garbage on the serial line
    if mt == '1': return ['1', 'accepted']   # the set command was accepted 
    
    n = int(m[2:5].decode()) # message len including CRC

    c = int.from_bytes(m[-3:-1], 'big') # CRC for the message
    b = m[5:]

    if len(b) != n: return ['0', 'MSG len malformed']

    b = m[5:-3]    # data buffer excluding CRC and '\r'
    if crc(b) != c: return ['0', 'CRC error']  # CRC doesn't match

    l = b.decode().split(',')
    return [mt] + l

