from typing import Any, Optional
from agiflow.opentelemetry.convention import SpanAttributes
from agiflow.opentelemetry.tracing.context import (
    get_prompt_key,
    get_prompt_template_variables,
    get_prompt_version,
    get_prompt_version_hash,
    get_prompt_version_name,
    get_workflow_name,
)
from opentelemetry.context import Context


def set_workflow_name_from_context(span, context: Optional[Context] = None):
    workflow_name = get_workflow_name(context=context)
    if workflow_name is not None:
        span.set_attribute(SpanAttributes.AGIFLOW_SERVICE_NAME, workflow_name)


def set_prompt_attributes_from_context(span, context: Optional[Context] = None):
    prompt_key = get_prompt_key(context=context)
    if prompt_key is not None:
        span.set_attribute(SpanAttributes.AGIFLOW_PROMPT_KEY, prompt_key)

    prompt_version = get_prompt_version(context=context)
    if prompt_version is not None:
        span.set_attribute(SpanAttributes.AGIFLOW_PROMPT_VERSION, prompt_version)

    prompt_version_name = get_prompt_version_name(context=context)
    if prompt_version_name is not None:
        span.set_attribute(SpanAttributes.AGIFLOW_PROMPT_VERSION_NAME, prompt_version_name)

    prompt_version_hash = get_prompt_version_hash(context=context)
    if prompt_version_hash is not None:
        span.set_attribute(SpanAttributes.AGIFLOW_PROMPT_VERSION_HASH, prompt_version_hash)

    prompt_template_variables: Any = get_prompt_template_variables(context=context)
    if prompt_version_hash is not None:
        for key, value in prompt_template_variables.items():
            span.set_attribute(
                f"{SpanAttributes.AGIFLOW_PROMPT_TEMPLATE_VARIABLES}.{key}", value
            )
