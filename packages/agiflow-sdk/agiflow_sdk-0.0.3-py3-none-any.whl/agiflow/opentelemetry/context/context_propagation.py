from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.context import get_current, set_value
from agiflow.opentelemetry.context import ContextKeys


def get_carrier_from_trace_context():
    carrier = {}
    context = get_current()
    TraceContextTextMapPropagator().inject(carrier)
    carrier[ContextKeys.ASSOCIATION_PROPERTIES] = context.get(ContextKeys.ASSOCIATION_PROPERTIES, {})
    carrier[ContextKeys.PROMPT_SETTINGS] = context.get(ContextKeys.PROMPT_SETTINGS, {})
    carrier[ContextKeys.WORKFLOW_NAME] = context.get(ContextKeys.WORKFLOW_NAME, {})
    carrier[ContextKeys.OVERRIDE_ENABLE_CONTENT_TRACING] = context.get(ContextKeys.OVERRIDE_ENABLE_CONTENT_TRACING, {})
    return carrier


def get_trace_context_from_carrier(carrier):
    ctx = TraceContextTextMapPropagator().extract(carrier)
    if carrier is not None:
        if carrier.get(ContextKeys.ASSOCIATION_PROPERTIES):
            ctx = set_value(ContextKeys.ASSOCIATION_PROPERTIES, carrier.get(ContextKeys.ASSOCIATION_PROPERTIES), ctx)
        if carrier.get(ContextKeys.PROMPT_SETTINGS):
            ctx = set_value(ContextKeys.PROMPT_SETTINGS, carrier.get(ContextKeys.PROMPT_SETTINGS), ctx)
        if carrier.get(ContextKeys.WORKFLOW_NAME):
            ctx = set_value(ContextKeys.WORKFLOW_NAME, carrier.get(ContextKeys.WORKFLOW_NAME), ctx)
        if carrier.get(ContextKeys.OVERRIDE_ENABLE_CONTENT_TRACING):
            ctx = set_value(
              ContextKeys.OVERRIDE_ENABLE_CONTENT_TRACING,
              carrier.get(ContextKeys.OVERRIDE_ENABLE_CONTENT_TRACING),
              ctx
            )
    return ctx
