from mage_ai.data_integrations.utils.settings import get_uuid
from mage_ai.shared.hash import index_by

SQL_SOURCES = [
    dict(
        name='Microsoft SQL Server',
        uuid='mssql',
    ),
    dict(name='MySQL'),
    dict(name='OracleDB'),
    dict(name='PostgreSQL'),
]

SQL_SOURCES_MAPPING = index_by(get_uuid, SQL_SOURCES)

SOURCES = sorted([
    dict(name='Api'),
    dict(name='Chargebee'),
    dict(name='GitHub'),
    dict(name='MongoDB'),
    dict(name='Mode'),
    dict(name='Sftp'),
] + SQL_SOURCES, key=lambda x: x['name'])
