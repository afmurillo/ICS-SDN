GRAVITATION = 9.81
TANK_DIAMETER = 1.38
TANK_SECTION = 1.5

PUMP_FLOWRATE_IN = 2.55				# Per hour
PUMP_FLOWRATE_OUT = 2.45			# Per hour

PH_PUMP_FLOWRATE_IN = 0.7
PH_PUMP_FLOWRATE_OUT = 0.7

PUMP_FLOWRATE_OUT_2 = 2.5


LIT_101_M = {
	'LL': 0.250,
	'L': 0.50,
	'H': 0.800,
	'HH': 1.200
}

PH_201_M = {
	'LL': 0.50,
	'L': 0.700,
	'H': 0.800,
	'HH': 1.000
}

LIT_301_M = {
	'LL': 0.250,
	'L': 0.50,
	'H': 0.800,
	'HH': 1.200
}

TANK_HEIGHT = 1.600

PLC_PERIOD_SEC = 0.4
PLC_PERIOD_HOURS = PLC_PERIOD_SEC/360.0
PLC_SAMPLES = 5000

PP_RESCALING_HOURS = 10
PP_PERIOD_SEC = 0.2
PP_PERIOD_HOURS = (PP_PERIOD_SEC / 3600.0) * PP_RESCALING_HOURS

PH_PERIOD_SEC = 0.05
PH_PERIOD_HOURS = (PH_PERIOD_SEC / 3600.0) * PP_RESCALING_HOURS

PP_SAMPLES = 4000

SAMPLE_TIME = 1

RWT_INIT_LEVEL = 0.200

IP = {
	'lit101': '192.168.1.10',
	'mv101': '192.168.1.11',
	'p101': '192.168.1.12',
	'plant101': '192.168.1.13',
	'plc101': '192.168.1.14',
	'ids101': '192.168.1.15',
	'sim101': '192.168.1.16',

	'fit201': '192.168.2.20',
	'ph201': '192.168.2.21',
	'p201': '192.168.2.22',
	'plant201': '192.168.2.23',
	'plc201': '192.168.2.24',
	'ids201': '192.168.2.25',
	'sim201': '192.168.2.26',

	'lit301': '192.168.3.27',
	'p301': '192.168.3.28',
	'plant301': '192.168.3.29',
	'plc301': '192.168.3.30',
	'ids301': '192.168.3.31',
	'sim301': '192.168.3.32',

	'controller': '192.168.56.100',
	'HMI':'192.168.0.10'

}

PORTS = {
	'controller_ids_port' : '5543',
	'plc_backup ' : '4234',
	'plc101_lit301' : '8754',
	'mvport' : '9587',
	'pport' : '7842'

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
	('MV101', 1, 'INT'),
	('LIT101', 1, 'REAL'),
	('P101', 1, 'INT'),
)

LOOP_2_TAGS = (
	('PH201', 2, 'REAL'),
	('FIT201', 2, 'REAL'),
	('P201', 2, 'INT'),
)

LOOP_3_TAGS = (
	('LIT301', 3, 'REAL'),
	('P301', 3, 'INT'),
)

################################################ Loop 1 Sensor and Protocols

LIT101_SERVER = {
	'address': IP['lit101'],
	'tags': LOOP_1_TAGS
}

LIT101_PROTOCOL = {
	'name': 'enip',
	'mode': 1,
	'server': LIT101_SERVER
}

MV101_SERVER = {
	'address': IP['mv101'],
	'tags': LOOP_1_TAGS
}
MV101_PROTOCOL = {
	'name': 'enip',
	'mode': 1,
	'server': MV101_SERVER
}

P101_SERVER = {
	'address': IP['p101'],
	'tags': LOOP_1_TAGS
}
P101_PROTOCOL = {
	'name': 'enip',
	'mode': 1,
	'server': P101_SERVER
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


################################################ Loop 2 Sensor and Protocols


FIT201_SERVER = {
	'address': IP['fit201'],
	'tags': LOOP_2_TAGS
}

FIT201_PROTOCOL = {
	'name': 'enip',
	'mode': 1,
	'server': FIT201_SERVER
}

PH201_SERVER = {
	'address': IP['ph201'],
	'tags': LOOP_2_TAGS
}

PH201_PROTOCOL = {
	'name': 'enip',
	'mode': 1,
	'server': PH201_SERVER
}

P201_SERVER = {
	'address': IP['p201'],
	'tags': LOOP_2_TAGS
}
P201_PROTOCOL = {
	'name': 'enip',
	'mode': 1,
	'server': P201_SERVER
}


PLC201_SERVER = {
	'address': IP['plc201'],
	'tags': LOOP_2_TAGS
}
PLC201_PROTOCOL = {
	'name': 'enip',
	'mode': 1,
	'server': PLC201_SERVER
}

IDS201_SERVER = {
	'address': IP['ids201'],
	'tags': LOOP_2_TAGS
}
IDS201_PROTOCOL = {
	'name': 'enip',
	'mode': 1,
	'server': IDS201_SERVER
}

SIM201_SERVER = {
	'address': IP['sim201'],
	'tags': LOOP_2_TAGS
}

SIM201_PROTOCOL = {
	'name': 'enip',
	'mode': 1,
	'server': SIM201_SERVER
}

################################################ Loop 3 Sensor and Protocols


LIT301_SERVER = {
	'address': IP['lit301'],
	'tags': LOOP_3_TAGS
}

LIT301_PROTOCOL = {
	'name': 'enip',
	'mode': 1,
	'server': LIT301_SERVER
}

P301_SERVER = {
	'address': IP['p301'],
	'tags': LOOP_3_TAGS
}
P301_PROTOCOL = {
	'name': 'enip',
	'mode': 1,
	'server': P301_SERVER
}

PLC301_SERVER = {
	'address': IP['plc301'],
	'tags': LOOP_3_TAGS
}
PLC301_PROTOCOL = {
	'name': 'enip',
	'mode': 1,
	'server': PLC301_SERVER
}

IDS301_SERVER = {
	'address': IP['ids301'],
	'tags': LOOP_3_TAGS
}

IDS301_PROTOCOL = {
	'name': 'enip',
	'mode': 1,
	'server': IDS301_SERVER
}

SIM301_SERVER = {
	'address': IP['sim301'],
	'tags': LOOP_3_TAGS
}

SIM301_PROTOCOL = {
	'name': 'enip',
	'mode': 1,
	'server': SIM301_SERVER
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
	INSERT INTO industry VALUES ('MV101', 1, '0');
	INSERT INTO industry VALUES ('P101', 1, '0');
	INSERT INTO industry VALUES ('LIT101', 1, '0.600');
	INSERT INTO industry VALUES ('FIT201', 2, '0');
	INSERT INTO industry VALUES ('PH201', 2, '0.700');
	INSERT INTO industry VALUES ('P201', 2, '0');
	INSERT INTO industry VALUES ('LIT301', 3, '0.600');
	INSERT INTO industry VALUES ('P301', 3, '0');
"""
