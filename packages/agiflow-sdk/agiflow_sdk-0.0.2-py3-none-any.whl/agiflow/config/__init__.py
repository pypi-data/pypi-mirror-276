from agiflow.config.environment_vars import EnvironmentVars


def is_tracing_enabled() -> bool:
    return EnvironmentVars.AGIFLOW_TRACING_ENABLED.lower() == "true"


def is_content_tracing_enabled() -> bool:
    return EnvironmentVars.AGIFLOW_TRACE_CONTENT.lower() == "true"


def is_metrics_enabled() -> bool:
    return EnvironmentVars.AGIFLOW_METRICS_ENABLED.lower() == "true"


def is_console_log_enabled() -> bool:
    return EnvironmentVars.AGIFLOW_SUPPRESS_WARNINGS.lower() == "true"


def is_using_global_provider() -> bool:
    return EnvironmentVars.AGIFLOW_OTEL_PYTHON_TRACER_PROVIDER_GLOBAL.lower() == "true"
