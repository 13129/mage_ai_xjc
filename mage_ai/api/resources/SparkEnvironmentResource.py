from mage_ai.api.resources.GenericResource import GenericResource
from mage_ai.api.resources.mixins.spark import SparkApplicationChild


class SparkEnvironmentResource(GenericResource, SparkApplicationChild):
    @classmethod
    async def member(cls, _pk, user, **kwargs):
        return cls(
            await cls.build_api().environment(),
            user,
            **kwargs,
        )
