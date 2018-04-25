import numpy as np 
from scipy.integrate import odeint 
import matplotlib.pyplot as plt 
import math

def francisco_model(l,t,q):

  Q1, Q2 = q
  L1, L2, L3 = l
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
  
  f = [L1,
      Q1 - u13*sn*np.sign(L1-L3)*math.sqrt(2*g*(L1-L3)),
      L2,
      Q2 + u32*sn*np.sign(L3-L2)*math.sqrt(abs(2*g*(L3-L2)))  - u20*sn*math.sqrt(2*g*L2),
      L3,
      u13*sn*np.sign(L1-L3)*math.sqrt(2*g*(L1-L3)) - u32*sn*np.sign(L3-L2)*math.sqrt(abs(2*g*(L3-L2)))
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

t = np.linspace(start=0, stop=1, num=100)
Q1 = mu13*sn*math.sqrt(2*g*(Y10-Y30));
Q2 = mu20*sn*math.sqrt(2*g*Y20)-mu32*sn*math.sqrt(2*g*(Y30-Y20));
q = [Q1, Q2]
l0 = [0.400, 0.200, 0.400]
wsol = odeint(francisco_model, l0, t, args=(q,),atol=abserr, rtol=relerr)

# Print the solution.
for t1, w1 in zip(t, wsol):
 print t1, w1[0], w1[1], w1[2]
