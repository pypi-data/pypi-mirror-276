import os
import sys

from typing import Any, Optional
from colorama import Fore
from opentelemetry.sdk.trace import SpanProcessor
from opentelemetry.sdk.trace.export import SpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, SERVICE_VERSION, TELEMETRY_SDK_NAME, TELEMETRY_SDK_VERSION
from opentelemetry.sdk.trace.sampling import Sampler
from opentelemetry.util.re import parse_env_headers
from agiflow.opentelemetry.convention import SpanAttributes
from agiflow.opentelemetry.types import DisableInstrumentations
from opentelemetry.propagators.textmap import TextMapPropagator

from agiflow.opentelemetry.trace_store import get_current_span
from agiflow.telemetry import Telemetry
from agiflow.config import (
    is_content_tracing_enabled,
    is_tracing_enabled,
)
from agiflow.services.fetch import Fetcher
from agiflow.opentelemetry.tracing.tracing import (
    TracerWrapper,
)
from agiflow.opentelemetry.tracing.context import (
    set_association_properties,
)
from agiflow.version import __version__
from agiflow.config.environment_vars import EnvironmentVars
from agiflow.opentelemetry import SDK_NAME
from typing import Dict


class Agiflow:
    __tracer_wrapper: TracerWrapper
    __fetcher: Fetcher

    @staticmethod
    def init(
        app_name: Optional[str] = sys.argv[0],
        app_version: Optional[str] = None,
        api_endpoint: str = "https://analytics-api.agiflow.io",
        api_key: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        exporter: Optional[SpanExporter] = None,
        resource_attributes: dict = {},
        disable_instrumentations: Optional[DisableInstrumentations] = None,
        propagator: Optional[TextMapPropagator] = None,
        Processor: Optional[type[SpanProcessor]] = None,
        sampler: Optional[Sampler] = None,
    ) -> None:
        Telemetry()

        api_endpoint = EnvironmentVars.AGIFLOW_BASE_URL or api_endpoint
        api_key = EnvironmentVars.AGIFLOW_API_KEY or api_key

        headersConf = Agiflow.get_header(headers)
        if not exporter and headersConf:
            print(
                Fore.GREEN
                + f"Agiflow exporting traces to {api_endpoint}, authenticating with custom headers"
            )

        if api_key and not exporter and not headersConf:
            print(
                Fore.GREEN
                + f"Agiflow exporting traces to {api_endpoint} authenticating with bearer token"
            )
            headersConf = {
                "Authorization": f"Bearer {api_key}",
            }

        if api_key:
            Agiflow.__fetcher = Fetcher(base_url=api_endpoint, api_key=api_key)

        if not is_tracing_enabled():
            print(Fore.YELLOW + "Tracing is disabled" + Fore.RESET)
            return

        enable_content_tracing = is_content_tracing_enabled()

        print(Fore.RESET)

        # Tracer init
        resource_attributes.update({
          SERVICE_NAME: app_name,
          SERVICE_VERSION: app_version,
          TELEMETRY_SDK_NAME: SDK_NAME,
          TELEMETRY_SDK_VERSION: __version__,
        })
        TracerWrapper.set_static_params(
            resource_attributes, enable_content_tracing, api_endpoint, headersConf
        )
        Agiflow.__tracer_wrapper = TracerWrapper(
            disable_instrumentations=disable_instrumentations,
            Processor=Processor,
            propagator=propagator,
            exporter=exporter,
            sampler=sampler
        )

    @staticmethod
    def get_header(headers: Optional[Dict[str, str]]):
        headersConf: Any = EnvironmentVars.AGIFLOW_HEADERS or headers or {}

        if isinstance(headersConf, str):
            headersConf = parse_env_headers(headersConf)

        return headersConf

    @staticmethod
    def set_association_properties(properties: dict) -> None:
        set_association_properties(properties)

    @staticmethod
    def report_score(
        id: Optional[str],
        score: float,
    ):
        """Apply score to all llm steps belongs to action
        id: action_id or unique id linked by associate_trace method
        """
        if not Agiflow.__fetcher:
            print(
                Fore.RED
                + "Error: Cannot report score. Missing Agiflow API key,"
                + " go to https://app.agiflow.com/settings/api-keys to create one"
            )
            print("Set the AGIFLOW_API_KEY environment variable to the key")
            print(Fore.RESET)
            return

        Agiflow.__fetcher.patch(
            f"actions/{id}/score",
            {
                "score": score,
            },
        )

    @staticmethod
    def associate_trace(id: str, span_id: Optional[str]):
        """Associate trace and space with a unique id
        id: unique id linked with trace
        span_id: unique id linked with span
        """
        span = get_current_span()
        span.set_attribute(
          f"{SpanAttributes.AGIFLOW_ASSOCIATION_PROPERTIES}.trace_alias",
          id
        )
        if span_id:
            span.set_attribute(
              f"{SpanAttributes.AGIFLOW_ASSOCIATION_PROPERTIES}.span_alias",
              span_id
            )

    @staticmethod
    def update_span(id: str, body: Dict[str, str]):
        """Update span value with data if processed asynchronously
        id: span_id or unique id linked with span
        """
        if not Agiflow.__fetcher:
            print(
                Fore.RED
                + "Error: Cannot report score. Missing Agiflow API key,"
                + " go to https://app.agiflow.com/settings/api-keys to create one"
            )
            print("Set the AGIFLOW_API_KEY environment variable to the key")
            print(Fore.RESET)
            return

        Agiflow.__fetcher.patch(
            f"steps/{id}",
            body,
        )
