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

# settings status
_d_stsb = {b'0': 'Nothing changed', b'1': 'Something changed'}
def stsb(b: bytes): return _d_stsb[b]

# charger status
_d_chst = {b'0': 'abnormal', b'1': 'normal but not charging', b'2': 'charging'}
def chsb(b: bytes): return _d_chst[b]

# load connection status 
_d_lc = {b'0': 'disconnect', b'1': 'connect'}
def lcsb(b: bytes): return _d_lc[b]

# batery charge/discharge
_d_bch = {b'0': 'donothing', b'1': 'charge', b'2': 'discharge'}
def bchsb(b: bytes): return _d_bch[b]

# AC-DC power direction
_d_dcac = {b'0': 'donothing', b'1': 'AC-DC', b'2': 'DC-AC'}
def dcacsb(b: bytes): return _d_dcac[b]

# line power direction
_d_lpd = {b'0': 'donothing', b'1': 'input', b'2': 'output'}
def lpdsb(b: bytes): return _d_lpd[b]


