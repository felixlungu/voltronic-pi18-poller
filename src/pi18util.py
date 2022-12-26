from datetime import datetime

# identity
def it(x): return x

# string from bytes
def sb(b: bytes): return b.decode()

# time from pi18 string 'YYYYmmDDHHMMSS'
def tb(b: bytes): return datetime.strptime(b.decode(), '%Y%m%d%H%M%S')

# string from 'NNxxxxxxx', NN number of bytes
def snb(b: bytes): return b[2:2+int(b[0:2])]

# int from string bytes b'12234'
def isb(b: bytes): return int(b.decode())

# float from scaled 1/10 int
def f10sb(b: bytes): return isb(b)/10

# float from scaled 1/1000 int (ex: Wh -> kWh)
def f1ksb(b: bytes): return isb(b)/1000
