from mage_ai.api.resources.GenericResource import GenericResource
from mage_ai.orchestration.db import safe_db_query


class EventRuleResource(GenericResource):
    @classmethod
    @safe_db_query
    def member(cls, pk, user, **kwargs):
        rules = []
        return cls(dict(rules=rules), user, **kwargs)
