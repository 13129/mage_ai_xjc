from mage_ai.shared.enum import StrEnum

DEFAULT_BATCH_SIZE = 100
DEFAULT_TIMEOUT_MS = 500


class SourceType(StrEnum):
    ACTIVEMQ = 'activemq'
    INFLUXDB = 'influxdb'
    KAFKA = 'kafka'
    NATS = 'nats'
    KINESIS = 'kinesis'
    RABBITMQ = 'rabbitmq'
    MONGODB = 'mongodb'


class SinkType(StrEnum):
    ACTIVEMQ = 'activemq'
    DUMMY = 'dummy'
    ELASTICSEARCH = 'elasticsearch'
    INFLUXDB = 'influxdb'
    KAFKA = 'kafka'
    KINESIS = 'kinesis'
    MONGODB = 'mongodb'
    MSSQL = 'mssql'
    MYSQL = 'mysql'
    ORACLEDB = 'oracledb'
    POSTGRES = 'postgres'
    RABBITMQ = 'rabbitmq'
    TRINO = 'trino'


GENERIC_IO_SINK_TYPES = frozenset([
    SinkType.MSSQL,
    SinkType.MYSQL,
    SinkType.TRINO,
])
