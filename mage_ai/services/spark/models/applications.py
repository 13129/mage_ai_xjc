import json
import os
import urllib.parse
from dataclasses import dataclass
from typing import Dict, List

from mage_ai.services.spark.constants import ComputeServiceUUID
from mage_ai.services.spark.models.base import BaseSparkModel
from mage_ai.services.spark.utils import get_compute_service
from mage_ai.shared.hash import merge_dict


@dataclass
class ApplicationAttempt(BaseSparkModel):
    app_spark_version: str = None  # 3.5.0
    completed: bool = None  # False
    duration: int = None  # 3498195
    end_time: str = None  # 1969-12-31T23:59:59.999GMT
    end_time_epoch: int = None  # -1
    last_updated: str = None  # 2023-10-15T09:03:30.699GMT
    last_updated_epoch: int = None  # 1697360610699
    spark_user: str = None  # root
    start_time: str = None  # 2023-10-15T09:03:30.699GMT
    start_time_epoch: int = None  # 1697360610699


@dataclass
class Application(BaseSparkModel):
    id: str  # local-1697360611228
    attempts: List[ApplicationAttempt] = None
    attempts_count: int = None
    name: str = None  # my spark app
    spark_ui_url: str = None

    def __post_init__(self):
        if self.attempts and isinstance(self.attempts, list):
            arr = []
            for m in self.attempts:
                if m and isinstance(m, dict):
                    arr.append(ApplicationAttempt.load(**m))
                else:
                    arr.append(m)
            self.attempts = arr

    @classmethod
    def load(cls, **kwargs):
        payload = kwargs.copy() if kwargs else {}
        return super().load(**payload)

    @classmethod
    def __cache_file_path(cls):
        return os.path.join(cls.cache_dir_path(), 'applications.json')

    @classmethod
    def clear_cache(cls) -> None:
        if os.path.exists(cls.__cache_file_path()):
            os.remove(cls.__cache_file_path())

    @classmethod
    def cache_application(cls, application) -> None:
        os.makedirs(cls.cache_dir_path(), exist_ok=True)

        data = {}
        if os.path.exists(cls.__cache_file_path()):
            with open(cls.__cache_file_path()) as f:
                content = f.read()
                if content:
                    data.update(json.loads(content) or {})

        data.update({
            application.calculated_id(): application.to_dict(),
        })

        with open(cls.__cache_file_path(), 'w') as f:
            f.write(json.dumps(data))

    @classmethod
    def get_applications_from_cache(cls) -> Dict:
        data = {}

        if os.path.exists(cls.__cache_file_path()):
            with open(cls.__cache_file_path()) as f:
                content = f.read()
                if content:
                    for application_dict in json.loads(content).values():
                        application = cls.load(**application_dict)
                        data[application.calculated_id()] = application

        return data

    def calculated_id(self) -> str:
        return self.id

    def to_dict(self, **kwargs) -> Dict:
        return merge_dict(
            super().to_dict(**kwargs),
            dict(calculated_id=self.calculated_id()),
        )
