from mage_ai.data_preparation.logging import LoggerType
from mage_ai.data_preparation.logging.logger_manager import LoggerManager
from mage_ai.data_preparation.repo_manager import RepoConfig


class LoggerManagerFactory:
    @classmethod
    def get_logger_manager(
        cls,
        repo_config: RepoConfig = None,
        **kwargs,
    ):
        return LoggerManager(repo_config=repo_config, **kwargs)
