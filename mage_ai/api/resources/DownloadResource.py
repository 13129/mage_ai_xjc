import datetime
from typing import Dict

import jwt

from mage_ai.api.constants import DOWNLOAD_TOKEN_LIFESPAN
from mage_ai.api.resources.GenericResource import GenericResource
from mage_ai.data_preparation.models.download import Download
from mage_ai.data_preparation.models.file import File
from mage_ai.data_preparation.models.pipeline import Pipeline
from mage_ai.orchestration.db import safe_db_query
from mage_ai.settings import JWT_DOWNLOAD_SECRET


class DownloadResource(GenericResource):

    @classmethod
    @safe_db_query
    async def create(cls, payload: Dict, user, **kwargs) -> 'DownloadResource':
        parent_model = kwargs.get('parent_model')

        ignore_folder_structure = payload.get('ignore_folder_structure', False)

        file_list = []

        if isinstance(parent_model, Pipeline):
            file_name, file_list = cls.fetch_pipeline_files(parent_model)
        elif isinstance(parent_model, File):
            if not parent_model.exists():
                raise Exception(f'File {parent_model.filename} does not exist.')
            file_name = parent_model.filename
            file_list.append(parent_model.file_path)

        token = cls.generate_download_token(file_name, file_list, ignore_folder_structure)
        download = Download(token)

        return cls(download, user)

    def fetch_pipeline_files(self: Pipeline):
        config_path = self.config_path

        zip_name = f'{self.uuid}.zip'
        file_list = [config_path] + [block.file_path for block in self.blocks_by_uuid.values()]

        return [zip_name, file_list]

    def generate_download_token(self, file_list, ignore_folder_structure):
        now = datetime.datetime.now()
        payload = {
            'file_name': self,
            'file_list': file_list,
            'ignore_folder_structure': ignore_folder_structure,
            'iat': now,
            'exp': now + datetime.timedelta(seconds=DOWNLOAD_TOKEN_LIFESPAN)
        }
        return jwt.encode(payload, JWT_DOWNLOAD_SECRET, algorithm="HS256")
