from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.context import get_current, set_value


def get_carrier_from_trace_context():
    carrier = {}
    context = get_current()
    TraceContextTextMapPropagator().inject(carrier)
    carrier['association_properties'] = context.get('association_properties', {})
    return carrier


def get_trace_context_from_carrier(carrier):
    ctx = TraceContextTextMapPropagator().extract(carrier)
    if carrier.get('association_properties'):
        ctx = set_value('association_properties', carrier.get('association_properties'), ctx)
    return ctx
