import math
import numpy as np
GRAVITATION = 9.81
TANK_DIAMETER = 1.38
TANK_SECTION = 1.5

PUMP_FLOWRATE_IN = 2.55				# Per hour
PUMP_FLOWRATE_OUT = 2.45			# Per hour

PH_PUMP_FLOWRATE_IN = 0.7
PH_PUMP_FLOWRATE_OUT = 0.7

PUMP_FLOWRATE_OUT_2 = 2.5

LOG_LIT101_FILE='./lit101.log'
LOG_LIT102_FILE='./lit102.log'
LOG_LIT103_FILE='./lit103.log'

LOG_PLC101_FILE='./plc101.log'

LOG_Q101_FILE='./q101.log'
LOG_Q102_FILE='./q102.log'

s = 0.0154
sn = 5e-5
mu13 = 0.5
mu32 = 0.5
mu20 = 0.675
QMAX = 1.2e-4
LJMAX = 0.62

W = math.sqrt(2*9.81)
g = 9.81

# Output Operation Points
Y10 = 0.400
Y20 = 0.200
Y30 = 0.300

# Input operating points (m3/s)
U10 = 0.350e-004
U20 = 0.375e-004

#Reference
#Y1 = 0.4 (t=1,200) 0.450 (t=201, 1500), 0.4 (t=1501, 2000)
#Y2 = 0.2 (t=1,400) 0.225 (t=401, 1700), 0.2 (t=1701, 2000)


#Q1 = mu13*sn*math.sqrt(2*g*(Y10-Y30)) + 0.4e-5;
Q1 = mu13*sn*math.sqrt(2*g*(Y10-Y30))
#%Q1o means Q1_operation = 3.5018e-5
#Q2 = mu20*sn*math.sqrt(2*g*Y20)-mu32*sn*math.sqrt(2*g*(Y30-Y20)) + 0.8e-5;
Q2 = mu20*sn*math.sqrt(2*g*Y20)-mu32*sn*math.sqrt(2*g*(Y30-Y20))

#%Q2o means Q2_operation = 3.1838e-5

# Tracking Controller Parameters
cte = 1e-4
K1 = np.array([[cte*21.6, cte*3, cte*-5],[cte*2.9, cte*19, cte*-4]])
K2 = np.array([[cte*-0.95, cte*-0.32], [cte*-0.30, cte*-0.91]])


# Matrices del Observador
Aobsv=np.array([[0.9899, 0.0005, 0.0098], [0.0004, 0.9804, 0.0095], [0.0108, 0.0107, 0.9784]])
Bobsv=np.array([[60.1584, 0.1660], [-0.3848, 60.1895], [0.4138, 0.1935]])
Cobsv=np.array([[1.0, 0.0, 0.0],[0.0, 1.0, 0.0]])
Gobsv=np.array([[0.9995, 0.0005],[0.0005, 0.9995],[52.7105, 48.2054]])


# Matrices de los otros observadores
F1 = np.array([[9.8990717e-01, 1.0003954e+00, 9.8418024e-03], [0.0000000e+00, 1.0000000e-03, 0.0000000e+00], [1.0844411e-02, -9.8940064e-01, 9.7837580e-01]])

T1 = np.array([[1.0000000e+00, -1.0000000e-04, 0.0000000e+00], [0.0000000e+00, 0.0000000e+00, 0.0000000e+00], [0.0000000e+00, -1.0000000e-04, 1.0000000e+00]])

B = np.array([[6.0158416e+01, 1.6595648e-01], [-3.8476906e-01, 6.0189541e+01], [4.1381529e-01, 1.9354159e-01]])

Ksp1 = np.array([[4.9535343e-04], [0.0000000e+00], [1.0698284e-02]])
Hsp1 = np.array([[1.0000000e-04],[1.0000000e+00], [1.0000000e-04]])

F2 = np.array([[1.0000000e-03, 0.0000000e+00, 0.0000000e+00], [-9.9973620e-01, 9.8040882e-01, 9.4916516e-03], [-9.8925454e-01, 1.0697354e-02, 9.7837576e-01]])

T2 = np.array([[0.0000000e+00, 0.0000000e+00, 0.0000000e+00], [-1.0000000e-04, 1.0000000e+00, 0.0000000e+00], [-1.0000000e-04, 0.0000000e+00, 1.0000000e+00]])

Ksp2 = np.array([[0.0000000e+00], [3.6278938e-04], [1.0844364e-02]])
Hsp2 = np.array([[1.0000000e+00], [1.0000000e-04], [1.0000000e-04]])

TANK_HEIGHT = 1.600

PLC_PERIOD_SEC = 1
LIT_PERIOD_SEC = 0.02
PLC_PERIOD_HOURS = PLC_PERIOD_SEC/360.0
PLC_SAMPLES = 500
LIT_SAMPLES = (PLC_PERIOD_SEC/LIT_PERIOD_SEC) * PLC_SAMPLES
PP_SAMPLES = 500

PP_RESCALING_HOURS = 10
PP_PERIOD_SEC = 0.2
PP_PERIOD_HOURS = (PP_PERIOD_SEC / 3600.0) * PP_RESCALING_HOURS

PH_PERIOD_SEC = 0.05
PH_PERIOD_HOURS = (PH_PERIOD_SEC / 3600.0) * PP_RESCALING_HOURS


SAMPLE_TIME = 1

RWT_INIT_LEVEL = 0.200

IP = {
	'lit101': '192.168.1.10',
	'q101': '192.168.1.11',
	'q102': '192.168.1.12',
	'plant101': '192.168.1.13',
	'plc101': '192.168.1.14',
	'ids101': '192.168.1.15',
	'sim101': '192.168.1.16',
	'p102' : '192.168.1.17',
	'lit102' : '192.168.1.18',
	'lit103' : '192.168.1.19',
	'controller': '192.168.56.100'
}

PORTS = {
	'controller_ids_port' : '5543',
	'plc_backup ' : '4234',
	'plc101_lit301' : '8754',
	'mvport' : '9587',
	'pport' : '7842',
	'hmi_poll_port': '5000',
	'p301_port' : '6568'
}

DPCTL_PORTS={ 
	'lit101' : '4',
	'ids101' : '5', 
	'plc101' : '5'
	}

NETMASK = '/24'


GENERIC_DATA = {
	'TODO': 'TODO',
}

# Loop Tags

LOOP_1_TAGS = (
	('LIT101', 1, 'REAL'),
	('LIT102', 1, 'REAL'),
	('LIT103', 1, 'REAL'),
	('Q101', 1, 'REAL'),
	('Q102', 1, 'REAL'),
)

################################################ Loop 1 Sensor and Protocols

TANK_SERVER = {
        'address': IP['plant101'],
        'tags': LOOP_1_TAGS
}


TANK_PROTOCOL = {
        'name': 'enip',
        'mode': 1,
        'server': TANK_SERVER
}

LIT101_SERVER = {
	'address': IP['lit101'],
	'tags': LOOP_1_TAGS
}

LIT101_PROTOCOL = {
	'name': 'enip',
	'mode': 1,
	'server': LIT101_SERVER
}

LIT102_SERVER = {
	'address': IP['lit102'],
	'tags': LOOP_1_TAGS
}

LIT102_PROTOCOL = {
	'name': 'enip',
	'mode': 1,
	'server': LIT102_SERVER
}

LIT103_SERVER = {
	'address': IP['lit103'],
	'tags': LOOP_1_TAGS
}

LIT103_PROTOCOL = {
	'name': 'enip',
	'mode': 1,
	'server': LIT103_SERVER
}


Q101_SERVER = {
	'address': IP['q101'],
	'tags': LOOP_1_TAGS
}
Q101_PROTOCOL = {
	'name': 'enip',
	'mode': 1,
	'server': Q101_SERVER
}

Q102_SERVER = {
	'address': IP['q102'],
	'tags': LOOP_1_TAGS
}

Q102_PROTOCOL = {
	'name': 'enip',
	'mode': 1,
	'server': Q102_SERVER
}

PLC101_SERVER = {
	'address': IP['plc101'],
	'tags': LOOP_1_TAGS
}
PLC101_PROTOCOL = {
	'name': 'enip',
	'mode': 1,
	'server': PLC101_SERVER
}

IDS101_SERVER = {
	'address': IP['ids101'],
	'tags': LOOP_1_TAGS
}
IDS101_PROTOCOL = {
	'name': 'enip',
	'mode': 1,
	'server': IDS101_SERVER
}

SIM101_SERVER = {
	'address': IP['sim101'],
	'tags': LOOP_1_TAGS
}

SIM101_PROTOCOL = {
	'name': 'enip',
	'mode': 1,
	'server': SIM101_SERVER
}


PATH = 'industry_db.sqlite'
NAME = 'industry'

STATE = {
	'name': NAME,
	'path': PATH
}

SCHEMA = """
CREATE TABLE industry (
	name		TEXT NOT NULL,
	pid		INTEGER NOT NULL,
	value		TEXT,
	PRIMARY KEY (name, pid)
);
"""

SCHEMA_INIT = """
	INSERT INTO industry VALUES ('Q101', 1, '0.0');
	INSERT INTO industry VALUES ('Q102', 1, '0.0');
	INSERT INTO industry VALUES ('LIT101', 1, '0.400');
	INSERT INTO industry VALUES ('LIT102', 1, '0.200');
	INSERT INTO industry VALUES ('LIT103', 1, '0.300');
"""
