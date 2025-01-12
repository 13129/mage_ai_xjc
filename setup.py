import setuptools


def readme():
    with open('README.md', encoding='utf8') as f:
        README = f.read()
    return README


requirements = []
with open('requirements.txt') as f:
    for line in f.read().splitlines():
        requirements.append(line)

setuptools.setup(
    name='mage-ai',
    # NOTE: when you change this, change the value of VERSION in the following file:
    # mage_ai/server/constants.py
    version='0.9.75',
    author='Mage',
    author_email='eng@mage.ai',
    description='Mage is a tool for building and deploying data pipelines.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='',
    packages=setuptools.find_packages('.'),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    install_requires=requirements,
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'mage=mage_ai.cli.main:app',
        ],
    },
    extras_require={
        'dbt': [
            'dbt-core==1.7.4',
            'dbt-postgres==1.7.4',
            'dbt-spark==1.7.1',
        ],
        'hdf5': [
            "tables==3.7.0; python_version < '3.11'",
            "tables==3.10.1; python_version >= '3.11'",
        ],
        'mysql': [
            "mysql-connector-python~=8.4.0; python_version < '3.11'",
            "mysql-connector-python~=9.0.0; python_version >= '3.11'",
        ],
        'oracle': [
            "oracledb==1.3.1; python_version < '3.12'",
            "oracledb==2.4.1; python_version >= '3.12'",
        ],
        'postgres': [
            'psycopg2==2.9.3',
            'psycopg2-binary==2.9.3',
            'sshtunnel==0.4.0',
        ],
        'spark': [
            'boto3==1.26.60',
            'botocore==1.29.60',
        ],
        'streaming': [
            'confluent-avro~=1.8.0',
            'elasticsearch==8.15.1',
            'kafka-python==2.0.2',
            'nats-py==2.6.0',
            'nkeys~=0.2.0',
            'pika==1.3.1',
            'pymongo==4.3.3',
            'stomp.py==8.1.0',
        ],
        'all': [
            'PyGithub==1.59.0',
            'astor>=0.8.1',
            'boto3==1.26.60',
            'botocore==1.29.60',
            'confluent-avro==1.8.0',
            'db-dtypes==1.0.5',
            'dbt-core==1.7.4',
            'dbt-postgres==1.7.4',
            'dbt-spark==1.7.1',
            'elasticsearch==8.15.1',
            'gspread==5.7.2',
            'kafka-python==2.0.2',
            'kubernetes>=28.1.0',
            'langchain==0.1.6',
            'langchain_community<0.0.20',
            'ldap3==2.9.1',
            'nats-py==2.6.0',
            'nkeys~=0.2.0',
            'opentelemetry-api==1.22.0',
            'opentelemetry-exporter-prometheus==0.43b0',
            'opentelemetry-instrumentation-tornado==0.43b0',
            'opentelemetry-exporter-otlp==1.22.0',
            'opentelemetry-instrumentation-sqlalchemy==0.43b0',
            'oracledb==1.3.1',
            'pika==1.3.1',
            'prometheus_client>=0.18.0',
            'protobuf>=4.25.0',
            'psycopg2-binary==2.9.3',
            'psycopg2==2.9.3',
            'pymongo==4.3.3',
            "pyodbc==4.0.35; python_version < '3.12'",
            "pyodbc==5.0.1; python_version >= '3.12'",
            'lxml==4.9.4',
            'sshtunnel==0.4.0',
            'stomp.py==8.1.0',
            'thefuzz[speedup]==0.19.0',
        ],
    },
)
