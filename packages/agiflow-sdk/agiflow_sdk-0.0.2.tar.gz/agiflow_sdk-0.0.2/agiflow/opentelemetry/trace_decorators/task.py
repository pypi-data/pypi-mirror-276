import json
from functools import wraps
from typing import Optional, Callable, Unpack

from agiflow.opentelemetry.convention import SpanAttributes, AgiflowSpanKindValues

from agiflow.opentelemetry.tracing import get_tracer
from agiflow.opentelemetry.tracing.tracing import TracerWrapper
from agiflow.utils import camel_to_snake, serialise_to_json

from agiflow.opentelemetry.trace_decorators.helper import (
    SharedKwargs,
    SharedKwargsWithHooks,
    add_extra_spans
)
from agiflow.opentelemetry.utils import (
    should_send_prompts,
)


def task(
    name: Optional[str] = None,
    method_name: Optional[str] = None,
    tlp_span_kind: Optional[AgiflowSpanKindValues] = AgiflowSpanKindValues.TASK,
    **kwargs: Unpack[SharedKwargsWithHooks]
):
    if method_name is None:
        return task_method(
            name=name,
            tlp_span_kind=tlp_span_kind,
            **kwargs
        )
    else:
        return task_class(
            name=name,
            method_name=method_name,
            tlp_span_kind=tlp_span_kind,
            **kwargs
        )


def task_method(
    name: Optional[str] = None,
    tlp_span_kind: Optional[AgiflowSpanKindValues] = None,
    input_serializer: Optional[Callable] = None,
    output_serializer: Optional[Callable] = None,
    **wkwargs: Unpack[SharedKwargs]
):
    def decorate(fn):
        @wraps(fn)
        def wrap(*args, **kwargs):
            if not TracerWrapper.verify_initialized():
                return fn(*args, **kwargs)

            if tlp_span_kind is None:
                span_kind = AgiflowSpanKindValues.TASK.value
            else:
                span_kind = tlp_span_kind.value

            span_name = (
                f"{name}.{span_kind}"
                if name
                else f"{fn.__name__}.{span_kind}"
            )
            with get_tracer() as tracer:
                with tracer.start_as_current_span(span_name) as span:
                    span.set_attribute(
                        SpanAttributes.AGIFLOW_SERVICE_TYPE, span_kind
                    )
                    if name:
                        span.set_attribute(SpanAttributes.AGIFLOW_ENTITY_NAME, name)
                    add_extra_spans(span, **wkwargs)

                    try:
                        if should_send_prompts():
                            if input_serializer:
                                input = input_serializer(*args, **kwargs)
                            else:
                                input = serialise_to_json({"args": args, "kwargs": kwargs})
                            span.set_attribute(
                                SpanAttributes.AGIFLOW_ENTITY_INPUT,
                                input,
                            )
                    except TypeError:
                        pass  # Some args might not be serializable

                    res = fn(*args, **kwargs)

                    try:
                        if should_send_prompts():
                            output = output_serializer(res) if output_serializer else json.dumps(res)
                            span.set_attribute(
                                SpanAttributes.AGIFLOW_ENTITY_OUTPUT,
                                output
                            )
                    except TypeError:
                        pass  # Some outputs might not be serializable

                    return res

        return wrap

    return decorate


def task_class(
    name: Optional[str],
    method_name: str,
    tlp_span_kind: Optional[AgiflowSpanKindValues] = AgiflowSpanKindValues.TASK,
    **kwargs: Unpack[SharedKwargsWithHooks]
):
    def decorator(cls):
        task_name = name if name else camel_to_snake(cls.__name__)
        method = getattr(cls, method_name)
        setattr(
            cls,
            method_name,
            task_method(name=task_name, tlp_span_kind=tlp_span_kind, **kwargs)(method),
        )
        return cls

    return decorator


# Async Decorators
def atask(
    name: Optional[str] = None,
    method_name: Optional[str] = None,
    tlp_span_kind: Optional[AgiflowSpanKindValues] = AgiflowSpanKindValues.TASK,
    **kwargs: Unpack[SharedKwargsWithHooks]
):
    if method_name is None:
        return atask_method(name=name, tlp_span_kind=tlp_span_kind, **kwargs)
    else:
        return atask_class(
            name=name, method_name=method_name, tlp_span_kind=tlp_span_kind, **kwargs
        )


def atask_method(
    name: Optional[str] = None,
    tlp_span_kind: Optional[AgiflowSpanKindValues] = AgiflowSpanKindValues.TASK,
    input_serializer: Optional[Callable] = None,
    output_serializer: Optional[Callable] = None,
    **wkwargs: Unpack[SharedKwargs]
):
    def decorate(fn):
        @wraps(fn)
        async def wrap(*args, **kwargs):
            if not TracerWrapper.verify_initialized():
                return await fn(*args, **kwargs)

            if tlp_span_kind is None:
                span_kind = AgiflowSpanKindValues.TASK.value
            else:
                span_kind = tlp_span_kind.value

            span_name = (
                f"{name}.{span_kind}"
                if name
                else f"{fn.__name__}.{span_kind}"
            )
            with get_tracer() as tracer:
                with tracer.start_as_current_span(span_name) as span:
                    span.set_attribute(
                        SpanAttributes.AGIFLOW_SERVICE_TYPE, span_kind
                    )
                    if name:
                        span.set_attribute(SpanAttributes.AGIFLOW_ENTITY_NAME, name)
                    add_extra_spans(span, **wkwargs)

                    try:
                        if should_send_prompts():
                            if input_serializer:
                                input = input_serializer(*args, **kwargs)
                            else:
                                input = serialise_to_json({"args": args, "kwargs": kwargs})
                            span.set_attribute(
                                SpanAttributes.AGIFLOW_ENTITY_INPUT,
                                input,
                            )
                    except TypeError:
                        pass  # Some args might not be serializable

                    res = await fn(*args, **kwargs)

                    try:
                        if should_send_prompts():
                            output = output_serializer(res) if output_serializer else json.dumps(res)
                            span.set_attribute(
                                SpanAttributes.AGIFLOW_ENTITY_OUTPUT,
                                output,
                            )
                    except TypeError:
                        pass  # Some args might not be serializable

                    return res

        return wrap

    return decorate


def atask_class(
    name: Optional[str],
    method_name: str,
    tlp_span_kind: Optional[AgiflowSpanKindValues] = AgiflowSpanKindValues.TASK,
    **kwargs: Unpack[SharedKwargsWithHooks]
):
    def decorator(cls):
        task_name = name if name else camel_to_snake(cls.__name__)
        method = getattr(cls, method_name)
        setattr(
            cls,
            method_name,
            atask_method(name=task_name, tlp_span_kind=tlp_span_kind, **kwargs)(method),
        )
        return cls

    return decorator


def agent(name: Optional[str] = None, method_name: Optional[str] = None, **kwargs: Unpack[SharedKwargsWithHooks]):
    return task(
        name=name, method_name=method_name, tlp_span_kind=AgiflowSpanKindValues.AGENT, **kwargs
    )


def tool(name: Optional[str] = None, method_name: Optional[str] = None, **kwargs: Unpack[SharedKwargsWithHooks]):
    return task(
        name=name, method_name=method_name, tlp_span_kind=AgiflowSpanKindValues.TOOL, **kwargs
    )


def aagent(name: Optional[str] = None, method_name: Optional[str] = None, **kwargs: Unpack[SharedKwargsWithHooks]):
    return atask(
        name=name, method_name=method_name, tlp_span_kind=AgiflowSpanKindValues.AGENT, **kwargs
    )


def atool(name: Optional[str] = None, method_name: Optional[str] = None, **kwargs: Unpack[SharedKwargsWithHooks]):
    return atask(
        name=name, method_name=method_name, tlp_span_kind=AgiflowSpanKindValues.TOOL, **kwargs
    )
