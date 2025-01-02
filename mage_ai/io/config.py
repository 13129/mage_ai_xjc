import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Union

import yaml
from jinja2 import Template

from mage_ai.data_preparation.shared.utils import get_template_vars
from mage_ai.settings.repo import get_repo_path
from mage_ai.shared.enum import StrEnum


class ConfigKey(StrEnum):
    """
    List of configuration settings for use with data IO clients.
    """

    # ALGOLIA_APP_ID = 'ALGOLIA_APP_ID'
    # ALGOLIA_API_KEY = 'ALGOLIA_API_KEY'
    # ALGOLIA_INDEX_NAME = 'ALGOLIA_INDEX_NAME'

    # CHROMA_COLLECTION = 'CHROMA_COLLECTION'
    # CHROMA_PATH = 'CHROMA_PATH'
    MOTHERDUCK_TOKEN = 'MOTHERDUCK_TOKEN'

    MONGODB_COLLECTION = 'MONGODB_COLLECTION'
    MONGODB_CONNECTION_STRING = "MONGODB_CONNECTION_STRING"
    MONGODB_DATABASE = 'MONGODB_DATABASE'
    MONGODB_HOST = 'MONGODB_HOST'
    MONGODB_PASSWORD = 'MONGODB_PASSWORD'
    MONGODB_PORT = 'MONGODB_PORT'
    MONGODB_USER = 'MONGODB_USER'

    # MSSQL_DATABASE = 'MSSQL_DATABASE'
    # MSSQL_DRIVER = 'MSSQL_DRIVER'
    # MSSQL_HOST = 'MSSQL_HOST'
    # MSSQL_PASSWORD = 'MSSQL_PASSWORD'
    # MSSQL_PORT = 'MSSQL_PORT'
    # MSSQL_SCHEMA = 'MSSQL_SCHEMA'
    # MSSQL_USER = 'MSSQL_USER'

    MYSQL_CONNECTION_METHOD = 'MYSQL_CONNECTION_METHOD'
    MYSQL_DATABASE = 'MYSQL_DATABASE'
    MYSQL_HOST = 'MYSQL_HOST'
    MYSQL_PASSWORD = 'MYSQL_PASSWORD'
    MYSQL_PORT = 'MYSQL_PORT'
    MYSQL_USER = 'MYSQL_USER'

    ORACLEDB_USER = 'ORACLEDB_USER'
    ORACLEDB_PASSWORD = 'ORACLEDB_PASSWORD'
    ORACLEDB_HOST = 'ORACLEDB_HOST'
    ORACLEDB_PORT = 'ORACLEDB_PORT'
    ORACLEDB_SERVICE = 'ORACLEDB_SERVICE'
    ORACLEDB_MODE = 'ORACLEDB_MODE'

    PINOT_HOST = 'PINOT_HOST'
    PINOT_PASSWORD = 'PINOT_PASSWORD'
    PINOT_PATH = 'PINOT_PATH'
    PINOT_PORT = 'PINOT_PORT'
    PINOT_SCHEME = 'PINOT_SCHEME'
    PINOT_USER = 'PINOT_USER'

    # QDRANT_COLLECTION = 'QDRANT_COLLECTION'
    # QDRANT_PATH = 'QDRANT_PATH'

    POSTGRES_CONNECTION_METHOD = 'POSTGRES_CONNECTION_METHOD'
    POSTGRES_CONNECT_TIMEOUT = 'POSTGRES_CONNECT_TIMEOUT'
    POSTGRES_DBNAME = 'POSTGRES_DBNAME'
    POSTGRES_HOST = 'POSTGRES_HOST'
    POSTGRES_PASSWORD = 'POSTGRES_PASSWORD'
    POSTGRES_PORT = 'POSTGRES_PORT'
    POSTGRES_SCHEMA = 'POSTGRES_SCHEMA'
    POSTGRES_SSH_HOST = 'POSTGRES_SSH_HOST'
    POSTGRES_SSH_PASSWORD = 'POSTGRES_SSH_PASSWORD'
    POSTGRES_SSH_PKEY = 'POSTGRES_SSH_PKEY'
    POSTGRES_SSH_PORT = 'POSTGRES_SSH_PORT'
    POSTGRES_SSH_USERNAME = 'POSTGRES_SSH_USERNAME'
    POSTGRES_USER = 'POSTGRES_USER'

    # REDSHIFT_CLUSTER_ID = 'REDSHIFT_CLUSTER_ID'
    # REDSHIFT_DBNAME = 'REDSHIFT_DBNAME'
    # REDSHIFT_DBUSER = 'REDSHIFT_DBUSER'
    # REDSHIFT_HOST = 'REDSHIFT_HOST'
    # REDSHIFT_IAM_PROFILE = 'REDSHIFT_IAM_PROFILE'
    # REDSHIFT_PORT = 'REDSHIFT_PORT'
    # REDSHIFT_SCHEMA = 'REDSHIFT_SCHEMA'
    # REDSHIFT_TEMP_CRED_PASSWORD = 'REDSHIFT_TEMP_CRED_PASSWORD'
    # REDSHIFT_TEMP_CRED_USER = 'REDSHIFT_TEMP_CRED_USER'

    # SNOWFLAKE_ACCOUNT = 'SNOWFLAKE_ACCOUNT'
    # SNOWFLAKE_DEFAULT_DB = 'SNOWFLAKE_DEFAULT_DB'
    # SNOWFLAKE_DEFAULT_SCHEMA = 'SNOWFLAKE_DEFAULT_SCHEMA'
    # SNOWFLAKE_DEFAULT_WH = 'SNOWFLAKE_DEFAULT_WH'
    # SNOWFLAKE_PASSWORD = 'SNOWFLAKE_PASSWORD'
    # SNOWFLAKE_PRIVATE_KEY_PASSPHRASE = 'SNOWFLAKE_PRIVATE_KEY_PASSPHRASE'
    # SNOWFLAKE_PRIVATE_KEY_PATH = 'SNOWFLAKE_PRIVATE_KEY_PATH'
    # SNOWFLAKE_ROLE = 'SNOWFLAKE_ROLE'
    # SNOWFLAKE_TIMEOUT = 'SNOWFLAKE_TIMEOUT'
    # SNOWFLAKE_USER = 'SNOWFLAKE_USER'

    SPARK_CLUSTER = 'SPARK_CLUSTER'
    SPARK_DRIVER = 'SPARK_DRIVER'
    SPARK_ENDPOINT = 'SPARK_ENDPOINT'
    SPARK_HOST = 'SPARK_HOST'
    SPARK_METHOD = 'SPARK_METHOD'
    SPARK_ORGANIZATION = 'SPARK_ORGANIZATION'
    SPARK_PORT = 'SPARK_PORT'
    SPARK_SCHEMA = 'SPARK_SCHEMA'
    SPARK_SERVER_SIDE_PARAMETERS = 'SPARK_SERVER_SIDE_PARAMETERS'
    SPARK_TOKEN = 'SPARK_TOKEN'
    SPARK_USER = 'SPARK_USER'

    TRINO_CATALOG = 'TRINO_CATALOG'
    TRINO_HOST = 'TRINO_HOST'
    TRINO_PASSWORD = 'TRINO_PASSWORD'
    TRINO_PORT = 'TRINO_PORT'
    TRINO_SCHEMA = 'TRINO_SCHEMA'
    TRINO_USER = 'TRINO_USER'

    # WEAVIATE_ENDPOINT = 'WEAVIATE_ENDPOINT'
    # WEAVIATE_INSTANCE_API_KEY = 'WEAVIATE_INSTANCE_API_KEY'
    # WEAVIATE_INFERENCE_API_KEY = 'WEAVIATE_INFERENCE_API_KEY'
    # WEAVIATE_COLLECTION = 'WEAVIATE_COLLECTION'


class BaseConfigLoader(ABC):
    """
    Base configuration loader class. A configuration loader is a read-only storage of configuration
    settings. The source of the configuration settings is dependent on the specific loader.
    """

    @abstractmethod
    def contains(self, key: Union[ConfigKey, str], **kwargs) -> bool:
        """
        Checks if the configuration setting stored under `key` is contained.
        Args:
            key (Union[ConfigKey, str]): Name of the configuration setting to check existence of.

        Returns:
            bool: Returns true if configuration setting exists, otherwise returns false.
        """
        pass

    @abstractmethod
    def get(self, key: Union[ConfigKey, str], **kwargs) -> Any:
        """
        Loads the configuration setting stored under `key`.

        Args:
            key (Union[ConfigKey, str]): Name of the configuration setting to load

        Returns:
            Any: The configuration setting stored under `key` in the configuration manager. If key
                 doesn't exist, returns None.
        """
        pass

    def __contains__(self, key: Union[ConfigKey, str]) -> bool:
        return self.contains(key)

    def __getitem__(self, key: str) -> Any:
        return self.get(key)

class EnvironmentVariableLoader(BaseConfigLoader):
    def contains(self, env_var: Union[ConfigKey, str]) -> bool:
        """
        Checks if the environment variable is defined.
        Args:
            key (Union[ConfigKey, str]): Name of the configuration setting to check existence of.

        Returns:
            bool: Returns true if configuration setting exists, otherwise returns false.
        """
        return env_var in os.environ

    def get(self, env_var: Union[ConfigKey, str]) -> Any:
        """
        Loads the config setting stored under the environment variable
        `env_var`.

        Args:
            env_var (str): Name of the environment variable to load configuration setting from

        Returns:
            Any: The configuration setting stored under `env_var`
        """
        return os.getenv(env_var)


class VerboseConfigKey(StrEnum):
    """
    Config key headers for the verbose configuration file format.
    """
    PINOT = 'Pinot'
    POSTGRES = 'PostgreSQL'
    SPARK = 'Spark'


class ConfigFileLoader(BaseConfigLoader):
    KEY_MAP = {
        ConfigKey.PINOT_HOST: (VerboseConfigKey.PINOT, 'host'),
        ConfigKey.PINOT_USER: (VerboseConfigKey.PINOT, 'password'),
        ConfigKey.PINOT_PATH: (VerboseConfigKey.PINOT, 'path'),
        ConfigKey.PINOT_PORT: (VerboseConfigKey.PINOT, 'port'),
        ConfigKey.PINOT_SCHEME: (VerboseConfigKey.PINOT, 'scheme'),
        ConfigKey.PINOT_USER: (VerboseConfigKey.PINOT, 'user'),
        ConfigKey.POSTGRES_DBNAME: (VerboseConfigKey.POSTGRES, 'database'),
        ConfigKey.POSTGRES_HOST: (VerboseConfigKey.POSTGRES, 'host'),
        ConfigKey.POSTGRES_PASSWORD: (VerboseConfigKey.POSTGRES, 'password'),
        ConfigKey.POSTGRES_PORT: (VerboseConfigKey.POSTGRES, 'port'),
        ConfigKey.POSTGRES_SCHEMA: (VerboseConfigKey.POSTGRES, 'schema'),
        ConfigKey.POSTGRES_USER: (VerboseConfigKey.POSTGRES, 'user'),
        ConfigKey.SPARK_CLUSTER: (VerboseConfigKey.SPARK, 'cluster'),
        ConfigKey.SPARK_DRIVER: (VerboseConfigKey.SPARK, 'driver'),
        ConfigKey.SPARK_ENDPOINT: (VerboseConfigKey.SPARK, 'endpoint'),
        ConfigKey.SPARK_HOST: (VerboseConfigKey.SPARK, 'host'),
        ConfigKey.SPARK_METHOD: (VerboseConfigKey.SPARK, 'method'),
        ConfigKey.SPARK_ORGANIZATION: (VerboseConfigKey.SPARK, 'organization'),
        ConfigKey.SPARK_PORT: (VerboseConfigKey.SPARK, 'port'),
        ConfigKey.SPARK_SCHEMA: (VerboseConfigKey.SPARK, 'schema'),
        ConfigKey.SPARK_SERVER_SIDE_PARAMETERS: (
            VerboseConfigKey.SPARK, 'server_side_parameters'),
        ConfigKey.SPARK_TOKEN: (VerboseConfigKey.SPARK, 'token'),
        ConfigKey.SPARK_USER: (VerboseConfigKey.SPARK, 'user'),
    }

    def __init__(
        self,
        filepath: Union[os.PathLike, None] = None,
        profile: str = 'default',
        config: Union[Dict, None] = None,
    ) -> None:
        """
        Initializes IO Configuration loader. Input configuration file can have two formats:
        - Standard: contains a subset of the configuration keys specified in `ConfigKey`. This
          is the default and recommended format
        - Verbose: Instead of configuration keys, each profile stores an object of settings
          associated with each data migration client. This format was used in previous versions
          of this tool, and exists for backwards compatibility.

        Args:
            filepath (os.PathLike, optional): Path to IO configuration file.
            Defaults to '[repo_path]/io_config.yaml'
            profile (str, optional): Profile to load configuration settings from. Defaults to
                                        'default'.
        """
        self.version = None

        if config:
            self.config = config
        else:
            if filepath is None:
                filepath = os.path.join(get_repo_path(), 'io_config.yaml')
            self.filepath = Path(filepath)
            self.profile = profile
            with self.filepath.open('r') as fin:
                config_file = Template(fin.read()).render(
                    **get_template_vars(),
                )
                config = yaml.full_load(config_file)
                self.config = config[profile]
                self.version = config.get('version')

        self.use_verbose_format = any(
            source in self.config.keys() for source in VerboseConfigKey)

    def contains(self, key: Union[ConfigKey, str]) -> Any:
        """
        Checks if the configuration setting stored under `key` is contained.

        Args:
            key (str): Name of the configuration setting to check.

        Returns:
            (bool) Returns true if configuration setting exists, otherwise returns false
        """
        if self.use_verbose_format:
            return self.__traverse_verbose_config(key) is not None
        return key in self.config

    def get(self, key: Union[ConfigKey, str]) -> Any:
        """
        Loads the configuration setting stored under `key`.

        Args:
            key (str): Key name of the configuration setting to load

        Returns:
            (Any) Configuration setting corresponding to the given key.
        """
        if self.use_verbose_format:
            return self.__traverse_verbose_config(key)
        return self.config.get(key)

    def __traverse_verbose_config(self, key: Union[ConfigKey, str]) -> Any:
        """
        Traverses a configuration file in verbose format to fetch the
        value if exists; else returns None.
        """
        keys = self.KEY_MAP.get(key)
        if keys is None:
            return None
        branch = self.config
        for key in keys:
            if branch is None:
                return None
            branch = branch.get(key)
        return branch
