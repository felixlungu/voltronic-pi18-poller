import serial
import pi18get as P

p = '/dev/ttyUSB5'

s = serial.Serial(p, 2400)

pi = P.pi(s)

print('PI', pi)

pi = P.pi(s)

print('PI', pi)

pi = P.pi(s)

print('PI', pi)

id = P.id(s)
print('ID: ', id)


t = P.t(s)
print('T: ', t)
et = P.et(s)
print('ET: ', et)
