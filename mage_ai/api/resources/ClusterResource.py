from mage_ai.api.errors import ApiError
from mage_ai.api.resources.GenericResource import GenericResource
from mage_ai.cluster_manager.constants import ClusterType
from mage_ai.orchestration.db import safe_db_query
from mage_ai.server.active_kernel import get_active_kernel_name
from mage_ai.server.kernels import KernelName
from mage_ai.settings.repo import get_repo_path


class ClusterResource(GenericResource):
    @classmethod
    @safe_db_query
    def member(cls, pk, user, **kwargs):
        clusters = []
        return cls(dict(
            clusters=clusters,
            type=pk,
        ), user, **kwargs)

    @safe_db_query
    def update(self, payload, **kwargs):
        ...

