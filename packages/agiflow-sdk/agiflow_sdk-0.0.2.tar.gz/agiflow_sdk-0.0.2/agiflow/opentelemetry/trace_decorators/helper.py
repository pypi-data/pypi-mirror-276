from typing import NotRequired, Optional, Callable, TypedDict
from agiflow.opentelemetry.tracing.context import set_prompt_tracing_context
from agiflow.opentelemetry.convention import AgiflowSpanAttributes


class PromptSettingsKwargs(TypedDict):
    prompt_key: NotRequired[str]
    prompt_version: NotRequired[str]
    prompt_version_name: NotRequired[str]
    prompt_version_hash: NotRequired[str]
    prompt_template_variables: NotRequired[dict]


class SharedKwargs(PromptSettingsKwargs):
    description: NotRequired[str]


class SharedKwargsWithHooks(SharedKwargs):
    input_serializer: NotRequired[Callable]
    output_serializer: NotRequired[Callable]


def add_extra_spans(
    span,
    description: Optional[str] = None,
    prompt_key: Optional[str] = None,
    prompt_version: Optional[str] = None,
    prompt_version_name: Optional[str] = None,
    prompt_version_hash: Optional[str] = None,
    prompt_template_variables: Optional[dict] = None,
):
    if description is not None:
        span.set_attribute(AgiflowSpanAttributes.AGIFLOW_ENTITY_DESCRIPTION, description)

    set_prompt_tracing_context(
        key=prompt_key,
        version=prompt_version,
        version_name=prompt_version_name,
        version_hash=prompt_version_hash,
        template_variables=prompt_template_variables,
    )
