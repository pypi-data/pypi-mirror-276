from typing import NotRequired, Optional, Callable, TypedDict
from agiflow.opentelemetry.context import set_prompt_settings_context, PromptSettings
from agiflow.opentelemetry.convention import AgiflowSpanAttributes


class SharedKwargs(TypedDict):
    # Add description to workflow and task
    # to add more context for user to provide feedbacks
    description: NotRequired[str]
    # All span within workflow/task will receive the
    # prompt version, etc... from current span
    # Only LLM span actually store the prompt version
    prompt_settings: NotRequired[PromptSettings]


class SharedKwargsWithHooks(SharedKwargs):
    # Default input serialiser will try to serialize {args, kwargs}
    # Use this hook to input output and return what you need
    # Arguments: *args, **kwargs
    input_serializer: NotRequired[Callable]
    # If the default json serialiser does not work properly
    # Use this hook to parse output and return what you need
    # Arguments: *args, result=result, **kwargs
    output_serializer: NotRequired[Callable]
    # Using this to set context for current span and it's children
    # Return a carrier dictionary that you pass through to the message queue, etc...
    # Supported context passing: association_properties, prompt_settings
    context_parser: NotRequired[Callable]


def add_extra_spans(
    span,
    description: Optional[str] = None,
    prompt_settings: Optional[PromptSettings] = None,
):
    if description is not None:
        span.set_attribute(AgiflowSpanAttributes.AGIFLOW_ENTITY_DESCRIPTION, description)

    if prompt_settings is not None:
        set_prompt_settings_context(prompt_settings)
