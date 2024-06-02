from typing import TypedDict, NotRequired


class PromptSettings(TypedDict):
    key: NotRequired[str]
    version: NotRequired[str]
    version_name: NotRequired[str]
    version_hash: NotRequired[str]
    template_variables: NotRequired[dict]


class AssociationProperties(TypedDict):
    action_id: NotRequired[str]
    task_id: NotRequired[str]
    user_id: NotRequired[str]


class ContextKeys:
    CORRELATION_ID = "correlation_id"
    ASSOCIATION_PROPERTIES = "association_properties"
    WORKFLOW_NAME = "workflow_name"
    # Prompts
    PROMPT_SETTINGS = "prompt_settings"

    # Toggle flag
    OVERRIDE_ENABLE_CONTENT_TRACING = "override_enable_content_tracing"
