import numpy as np 
from scipy.integrate import odeint 
import matplotlib.pyplot as plt 
import math

def francisco_model(l,t,q):

  #l=[Y10, 0.0, Y20, 0.0, Y30]
  L1,L2, L3 = l
  Q1, Q2 = q
  s = 0.0154
  sn = 5e-5
  u13 = 0.5
  u32 = 0.5
  u20 = 0.675
  QMAX = 1.2e-4
  LJMAX = 0.62

  W = math.sqrt(2*9.81)
  g = 9.81

  f = [(Q1 - u13*sn*np.sign(L1-L3)*math.sqrt(2*g*abs(L1-L3)))/s,
       (Q2 + u32*sn*np.sign(L3-L2)*math.sqrt(abs(2*g*(L3-L2)))  - u20*sn*math.sqrt(2*g*L2))/s,
       (u13*sn*np.sign(L1-L3)*math.sqrt(2*g*abs(L1-L3)) - u32*sn*np.sign(L3-L2)*math.sqrt(abs(2*g*abs(L3-L2))))/s
      ]
  return f

s = 0.0154
sn = 5e-5
u13 = 0.5
u32 = 0.5
u20 = 0.6
QMAX = 1.5e-4
LJMAX = 0.62

mu13 = 0.5
mu20 = 0.675
mu32 = 0.5
W = math.sqrt(2*9.81)
g = 9.81
Y10 = 0.400
Y20 = 0.200
Y30 = 0.300

abserr = 1.0e-8
relerr = 1.0e-6
#t = np.linspace(start=0, stop=1, num=100)
stoptime = 1
numpoints = 100
t = [stoptime * float(i) / (numpoints - 1) for i in range(numpoints)]


Q1 = mu13*sn*math.sqrt(2*g*(Y10-Y30)) + 0.4e-5
Q2 = mu20*sn*math.sqrt(2*g*Y20)-mu32*sn*math.sqrt(2*g*(Y30-Y20)) + 0.8e-5
#Q1 = mu13*sn*math.sqrt(2*g*(Y10-Y30))
#Q2 = mu20*sn*math.sqrt(2*g*Y20)-mu32*sn*math.sqrt(2*g*(Y30-Y20))

l = [Y10, Y20, Y30]
#l=[Y10, 0.0, Y20, 0.0, Y30]
q=[Q1, Q2]

numsamples=20000

for i in range(numsamples):
	wsol = odeint(francisco_model, l, t, args=(q,),atol=abserr, rtol=relerr)
	#wsol entrega dy/dt
	l[0] =  wsol[-1][0]
	l[1] =  wsol[-1][1]
	l[2] =  wsol[-1][2]
	print i, " ", l[0], " ", l[1], " ", l[2]
#print Q1
#print Q2
