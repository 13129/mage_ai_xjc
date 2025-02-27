from typing import Dict

from mage_ai.data_preparation.decorators import collect_decorated_objs
from mage_ai.streaming.constants import GENERIC_IO_SINK_TYPES, SinkType


class SinkFactory:
    @classmethod
    def get_sink(cls, config: Dict, **kwargs):
        connector_type = config['connector_type']
        if connector_type == SinkType.ACTIVEMQ:
            from mage_ai.streaming.sinks.activemq import ActiveMQSink

            return ActiveMQSink(config, **kwargs)

        elif connector_type == SinkType.ELASTICSEARCH:
            from mage_ai.streaming.sinks.elasticsearch import ElasticSearchSink

            return ElasticSearchSink(config, **kwargs)
        elif connector_type == SinkType.INFLUXDB:
            from mage_ai.streaming.sinks.influxdb import InfluxDbSink

            return InfluxDbSink(config, **kwargs)
        elif connector_type == SinkType.KAFKA:
            from mage_ai.streaming.sinks.kafka import KafkaSink

            return KafkaSink(config, **kwargs)
        elif connector_type == SinkType.KINESIS:
            from mage_ai.streaming.sinks.kinesis import KinesisSink

            return KinesisSink(config, **kwargs)
        elif connector_type == SinkType.MONGODB:
            from mage_ai.streaming.sinks.mongodb import MongoDbSink

            return MongoDbSink(config, **kwargs)
        elif connector_type == SinkType.ORACLEDB:
            from mage_ai.streaming.sinks.oracledb import OracleDbSink

            return OracleDbSink(config, **kwargs)
        elif connector_type == SinkType.POSTGRES:
            from mage_ai.streaming.sinks.postgres import PostgresSink

            return PostgresSink(config, **kwargs)
        elif connector_type == SinkType.RABBITMQ:
            from mage_ai.streaming.sinks.rabbitmq import RabbitMQSink

            return RabbitMQSink(config, **kwargs)
        elif connector_type in GENERIC_IO_SINK_TYPES:
            from mage_ai.streaming.sinks.generic_io import GenericIOSink

            return GenericIOSink(config, **kwargs)
        raise Exception(
            f'Ingesting data to {connector_type} is not supported in streaming pipelines yet.',
        )

    @classmethod
    def get_python_sink(cls, content: str, **kwargs):
        """
        Find the class that's decorated with streaming_sink from the source code.

        Args:
            content (str): The python code that contains the streaming sink implementation.
            **kwargs: {'global_vars': {...}}

        Returns:
            The initialized class object.

        Raises:
            Exception: Description
        """
        decorated_sinks = []

        exec(content, {'streaming_sink': collect_decorated_objs(decorated_sinks)})

        if not decorated_sinks:
            raise Exception('Not find the class that has streaming_sink decorator.')

        return decorated_sinks[0](**kwargs)
