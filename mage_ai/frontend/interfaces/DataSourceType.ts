import { BlockTypeEnum } from './BlockType';

export enum DataSourceTypeEnum {
  ACTIVEMQ = 'activemq',
  API = 'api',
  ELASTICSEARCH = 'elasticsearch',
  FILE = 'file',
  GENERIC = 'generic',
  INFLUXDB = 'influxdb',
  KAFKA = 'kafka',
  KINESIS = 'kinesis',
  MONGODB = 'mongodb',
  MSSQL = 'mssql',
  MYSQL = 'mysql',
  NATS = 'nats',
  ORACLEDB = 'oracledb',
  PINOT = 'pinot',
  POSTGRES = 'postgres',
  RABBITMQ = 'rabbitmq',
  TRINO = 'trino',
}

export const DATA_SOURCE_TYPE_HUMAN_READABLE_NAME_MAPPING = {
  [DataSourceTypeEnum.ACTIVEMQ]: 'ActiveMQ',
  [DataSourceTypeEnum.API]: 'API',
  [DataSourceTypeEnum.ELASTICSEARCH]: 'ElasticSearch',
  [DataSourceTypeEnum.FILE]: 'Local file',
  [DataSourceTypeEnum.GENERIC]: 'Generic (no template)',
  [DataSourceTypeEnum.INFLUXDB]: 'InfluxDB',
  [DataSourceTypeEnum.KAFKA]: 'Kafka',
  [DataSourceTypeEnum.KINESIS]: 'Kinesis',
  [DataSourceTypeEnum.MONGODB]: 'MongoDB',
  [DataSourceTypeEnum.MSSQL]: 'Microsoft SQL Server',
  [DataSourceTypeEnum.MYSQL]: 'MySQL',
  [DataSourceTypeEnum.NATS]: 'NATS',
  [DataSourceTypeEnum.ORACLEDB]: 'OracleDB',
  [DataSourceTypeEnum.PINOT]: 'Pinot',
  [DataSourceTypeEnum.POSTGRES]: 'PostgreSQL',
  [DataSourceTypeEnum.RABBITMQ]: 'RabbitMQ',
  [DataSourceTypeEnum.TRINO]: 'Trino',
};

export const DATA_SOURCE_TYPES: { [blockType in BlockTypeEnum]?: DataSourceTypeEnum[] } = {
  [BlockTypeEnum.DATA_LOADER]: [
    DataSourceTypeEnum.GENERIC,
    DataSourceTypeEnum.FILE,
    DataSourceTypeEnum.API,
    DataSourceTypeEnum.MYSQL,
    DataSourceTypeEnum.ORACLEDB,
    DataSourceTypeEnum.PINOT,
    DataSourceTypeEnum.POSTGRES,
    DataSourceTypeEnum.MONGODB,
  ],
  [BlockTypeEnum.DATA_EXPORTER]: [
    DataSourceTypeEnum.GENERIC,
    DataSourceTypeEnum.FILE,
    DataSourceTypeEnum.MYSQL,
    DataSourceTypeEnum.POSTGRES,
  ],
  [BlockTypeEnum.TRANSFORMER]: [
    DataSourceTypeEnum.POSTGRES,
  ],
  [BlockTypeEnum.SENSOR]: [
    DataSourceTypeEnum.GENERIC,
    DataSourceTypeEnum.MYSQL,
    DataSourceTypeEnum.POSTGRES,
  ],
};

export default DataSourceTypeEnum;
