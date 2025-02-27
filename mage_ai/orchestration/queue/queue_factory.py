from mage_ai.data_preparation.repo_manager import get_repo_config
from mage_ai.orchestration.queue.config import QueueConfig, QueueType


class QueueFactory:
    queue = None

    @classmethod
    def get_queue(cls):
        if cls.queue is not None:
            return cls.queue

        queue_config = QueueConfig.load(config=get_repo_config().queue_config or dict())
        if queue_config.queue_type == QueueType.CELERY:
            from mage_ai.orchestration.queue.celery_queue import CeleryQueue
            cls.queue = CeleryQueue(queue_config)
        else:
            from mage_ai.orchestration.queue.process_queue import ProcessQueue
            cls.queue = ProcessQueue(queue_config)
        return cls.queue
