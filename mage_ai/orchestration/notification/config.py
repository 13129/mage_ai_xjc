from dataclasses import dataclass, field
from typing import List

from mage_ai.services.email.config import EmailConfig
from mage_ai.services.opsgenie.config import OpsgenieConfig
from mage_ai.shared.config import BaseConfig
from mage_ai.shared.enum import StrEnum


class AlertOn(StrEnum):
    PIPELINE_RUN_FAILURE = 'trigger_failure'
    PIPELINE_RUN_SUCCESS = 'trigger_success'
    PIPELINE_RUN_PASSED_SLA = 'trigger_passed_sla'


DEFAULT_ALERT_ON = [
    AlertOn.PIPELINE_RUN_FAILURE,
    AlertOn.PIPELINE_RUN_PASSED_SLA,
]


@dataclass
class MessageTemplate(BaseConfig):
    title: str = None
    summary: str = None
    details: str = None


@dataclass
class MessageTemplates(BaseConfig):
    success: MessageTemplate = None
    failure: MessageTemplate = None
    passed_sla: MessageTemplate = None


@dataclass
class NotificationConfig(BaseConfig):
    alert_on: List[AlertOn] = field(default_factory=lambda: DEFAULT_ALERT_ON)
    email_config: EmailConfig = None
    opsgenie_config: OpsgenieConfig = None
    message_templates: MessageTemplates = None
