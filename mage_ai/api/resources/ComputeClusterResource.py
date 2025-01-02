from mage_ai.api.resources.GenericResource import GenericResource
from mage_ai.services.compute.models import ComputeService
from mage_ai.services.spark.constants import ComputeServiceUUID


class ComputeClusterResource(GenericResource):
    @classmethod
    async def collection(self, query_arg, _meta, user, **kwargs):
        parent_model = kwargs.get('parent_model')

        include_all_states = query_arg.get('include_all_states', [None])
        if include_all_states:
            include_all_states = include_all_states[0]
        clusters = []
        return self.build_result_set(
            clusters,
            user,
            **kwargs,
        )

    @classmethod
    async def member(self, pk, user, **kwargs):
        parent_model = kwargs.get('parent_model')

        cluster = None
        return self(dict(
            cluster=cluster,
        ), user, **kwargs)

    @classmethod
    def create(self, payload, user, **kwargs):
        parent_model = kwargs.get('parent_model')

        cluster = None

        return self(dict(
            cluster=cluster,
        ), user, **kwargs)

    async def delete(self, **kwargs):
        parent_model = kwargs.get('parent_model')

        if isinstance(parent_model, ComputeService):
            ...

    async def update(self, payload, **kwargs):
        parent_model = kwargs.get('parent_model')

        if isinstance(parent_model, ComputeService):
            ...

    def get_cluster(self):
        return self.model.get('cluster')

    def get_cluster_id(self) -> str:
        cluster_id = None

        if 'cluster' in self.model:
            cluster = self.get_cluster()
            if cluster:
                cluster_id = None
                if isinstance(cluster, dict):
                    cluster_id = cluster.get('id')

        return cluster_id
