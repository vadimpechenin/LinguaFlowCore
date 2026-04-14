pl = 'nodocker'
#pl = 'docker'
if (pl=='docker'):
    # Для Docker
    DATABASE_URI = 'postgresql+psycopg2://postgres:mapr@host.docker.internal:5432/lfc'
else:
    DATABASE_URI = 'postgresql+psycopg2://postgres:mapr@localhost:5432/lfc'

nameOfDataBase = "lfc"

SQLDataBaseObj = None
MainHandlerObj = None
AllParametersObj = None
UUIDClassObj = None




