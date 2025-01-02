from mage_ai.api.resources.GenericResource import GenericResource
from mage_ai.services.compute.models import ComputeConnection, ComputeService
from mage_ai.services.spark.constants import ComputeServiceUUID
from mage_ai.shared.array import find


class ComputeConnectionResource(GenericResource):
    @classmethod
    async def collection(self, query_arg, _meta, user, **kwargs):
        parent_model = kwargs.get('parent_model')
        arr = []
        return self.build_result_set(
            arr,
            user,
            **kwargs,
        )

    @classmethod
    async def member(self, pk, user, **kwargs):
        parent_model = kwargs.get('parent_model')
        model = ComputeConnection.load(name=pk, uuid=pk)
        return self(model, user, **kwargs)

    async def update(self, payload, **kwargs):
        parent_model = kwargs.get('parent_model')

        action_uuid = payload.get('action')

        if not action_uuid:
            return

        if parent_model and isinstance(parent_model, ComputeService):
            ...
