import serial
import pi18get as P

p = '/dev/ttyUSB1'

s = serial.Serial(p, 2400)

pi = P.pi(s)

print('PI', pi)