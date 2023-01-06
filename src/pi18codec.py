
# vim:set sw=4 ts=4 et

def crc(b):
    cv = 0
    d = 0
    t = [0x0000, 0x1021, 0x2042, 0x3063, 0x4084, 0x50A5, 0x60C6, 0x70E7, 0x8108, 0x9129, 0xA14A, 0xB16B, 0xC18C, 0xD1AD, 0xE1CE, 0xF1EF]

    for c in b:
        d = ((cv >> 8) & 0xFF) >> 4
        cv = (cv << 4) & 0xFFFF
        i = d ^ (c >> 4)
        cv ^= t[i]
        d = ((cv >> 8) & 0xFF) >> 4
        cv = (cv << 4) & 0xFFFF
        i = d ^ (c & 0x0F)
        cv ^= t[i]

    cl = cv & 0xFF
    ch = (cv >> 8) & 0xFF
    if cl in [0x28, 0x0D, 0x0A]: cl+=1
    if ch in [0x28, 0x0D, 0x0A]: ch+=1
    return ch.to_bytes(1) + cl.to_bytes(1)

# encode a PI18 message:
#   m: ['P' or 'S', 'MGSGtype', values...]
# ex: enc(['P','EY','2022']) -> b'^P009EY2022\xe5\x9d\r
def enc(m):
    mt = m[0].encode()
    b = m[1].encode() + ','.join(str(x) for x in m[2:]).encode()
    n = len(b)
    s = b'^' + mt + ('%03d'%(n+3)).encode() + b
    c = crc(s)
    return s + c + b'\r'

# decode a PI18 message
# m: b'^D0251401234567890123456789p\xa2\r' -> ['D', '1401234567890123456789']
# first element is either '0' for error, '1' for accepted set msg or 'D' for query reply
def dec(m):
    if m[0:1] != b'^' or m[-1:] != b'\r': return ['0', 'malformed']

    mt = m[1:2].decode()
    if mt == '0': return ['0', 'NAK']   # rejected command: not implemented or garbage on the serial line
    if mt == '1': return ['1', 'ACK']   # the set command was accepted 
    
    n = int(m[2:5].decode()) # message len including CRC

    c = m[-3:-1] # CRC for the message
    if crc(m[:-3]) != c: return ['0', 'CRC error']  # CRC doesn't match

    b = m[5:]
    if len(b) != n: return ['0', 'MSG len malformed']

    b = m[5:-3]    # data buffer excluding CRC and '\r'

    l = b.split(b',')
    return [mt] + l