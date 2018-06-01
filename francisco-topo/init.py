from minicps.states import SQLiteState
from utils import PATH, SCHEMA, SCHEMA_INIT

if __name__ == "__main__":
	SQLiteState._create(PATH, SCHEMA)
	SQLiteState._init(PATH, SCHEMA_INIT)
