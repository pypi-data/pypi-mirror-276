"""
Copyright (c) 2024 AgiFlow

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from typing import Optional

import logging
from colorama import Fore
from opentelemetry.sdk.trace.sampling import Sampler
from opentelemetry.trace import ProxyTracerProvider
from opentelemetry.sdk.trace import TracerProvider, SpanProcessor
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    SpanExporter
)
from opentelemetry.sdk.resources import Resource
from opentelemetry.propagators.textmap import TextMapPropagator
from opentelemetry.propagate import set_global_textmap

from typing import Any, Callable, Dict
from agiflow.opentelemetry.convention import SpanAttributes
from agiflow.opentelemetry.types import DisableInstrumentations, InstrumentationType
from agiflow.opentelemetry.trace_exporter.json import OTLPJsonSpanExporter
from agiflow.opentelemetry.instrumentation import (
    LangchainInstrumentation,
    LangchainCommunityInstrumentation,
    LangchainCoreInstrumentation,
    OpenAIInstrumentation,
    AnthropicInstrumentation,
)
from agiflow.opentelemetry.trace_store import set_tracer_provider, get_tracer_provider
from agiflow.opentelemetry.tracing.content_alow_list import ContentAllowList
from agiflow.opentelemetry.tracing.context import set_override_enable_context_tracing, get_association_properties
from agiflow.opentelemetry.tracing.span_from_context import (
  set_workflow_name_from_context,
  set_prompt_attributes_from_context
)
from agiflow.version import __version__
from agiflow.config import is_console_log_enabled


TRACER_NAME = "agiflow.tracer"


class TracerWrapper(object):
    enable_content_tracing: bool = True
    resource_attributes: dict = {}
    endpoint: Optional[str] = None
    headers: Dict[str, str] = {}
    __resource: Resource
    __sampler: Optional[Sampler]
    __tracer_provider: TracerProvider
    __spans_processor: SpanProcessor
    __content_allow_list: ContentAllowList
    __spans_processor_original_on_start: Optional[Callable] = None

    def __new__(
        cls,
        propagator: Optional[TextMapPropagator] = None,
        disable_instrumentations: Optional[DisableInstrumentations] = None,
        exporter: Optional[SpanExporter] = None,
        Processor: Optional[type[SpanProcessor]] = None,
        sampler: Optional[Sampler] = None
    ) -> "TracerWrapper":
        if not hasattr(cls, "instance"):
            obj = cls.instance = super(TracerWrapper, cls).__new__(cls)
            if not TracerWrapper.endpoint:
                return obj

            obj.__resource = Resource(attributes=TracerWrapper.resource_attributes)
            obj.__sampler = sampler
            obj.__tracer_provider = init_tracer_provider(
                resource=obj.__resource,
                sampler=obj.__sampler,
            )

            if Processor is None:
                Processor = BatchSpanProcessor

            if exporter is None:
                span_exporter = init_spans_exporter(
                    TracerWrapper.endpoint, TracerWrapper.headers
                )
                obj.__spans_processor = Processor(span_exporter)
            else:
                obj.__spans_processor = Processor(exporter)

            obj.__spans_processor.on_start = obj._span_processor_on_start

            obj.__tracer_provider.add_span_processor(obj.__spans_processor)

            if propagator:
                set_global_textmap(propagator)

            all_instrumentations = {
                "openai": OpenAIInstrumentation(),
                "langchain": LangchainInstrumentation(),
                "langchain_core": LangchainCoreInstrumentation(),
                "langchain_community": LangchainCommunityInstrumentation(),
                "anthropic": AnthropicInstrumentation(),
            }

            init_instrumentations(disable_instrumentations, all_instrumentations, obj.__tracer_provider)
        return cls.instance

    def exit_handler(self):
        self.flush()

    def _span_processor_on_start(self, span, parent_context):
        set_workflow_name_from_context(span)

        association_properties: Any = get_association_properties()
        if association_properties is not None:
            for key, value in association_properties.items():
                span.set_attribute(
                    f"{SpanAttributes.AGIFLOW_ASSOCIATION_PROPERTIES}.{key}", value
                )

            if not self.enable_content_tracing:
                if self.__content_allow_list.is_allowed(association_properties):
                    set_override_enable_context_tracing(True)
                else:
                    set_override_enable_context_tracing(False)

        set_prompt_attributes_from_context(span)

        # Call original on_start method if it exists in custom processor
        if self.__spans_processor_original_on_start:
            self.__spans_processor_original_on_start(span, parent_context)

    @staticmethod
    def set_static_params(
        resource_attributes: dict,
        enable_content_tracing: bool,
        endpoint: str,
        headers: Dict[str, str],
    ) -> None:
        TracerWrapper.resource_attributes = resource_attributes
        TracerWrapper.enable_content_tracing = enable_content_tracing
        TracerWrapper.endpoint = endpoint
        TracerWrapper.headers = headers

    @classmethod
    def verify_initialized(cls) -> bool:
        if hasattr(cls, "instance"):
            return True

        if is_console_log_enabled():
            return False

        print(
            Fore.RED
            + "Warning: Agiflow not initialized, make sure you call Agiflow.init()"
        )
        print(Fore.RESET)
        return False

    def flush(self):
        self.__spans_processor.force_flush()

    def get_tracer(self):
        return self.__tracer_provider.get_tracer(TRACER_NAME, __version__)


def init_tracer_provider(resource: Resource, sampler: Optional[Sampler]) -> TracerProvider:
    provider: Optional[TracerProvider] = None
    default_provider: TracerProvider = get_tracer_provider()

    if isinstance(default_provider, ProxyTracerProvider):
        if sampler:
            provider = TracerProvider(resource=resource, sampler=sampler)
        else:
            provider = TracerProvider(resource=resource)

        set_tracer_provider(provider)
    elif not hasattr(default_provider, "add_span_processor"):
        logging.error(
            "Cannot add span processor to the default provider since it doesn't support it"
        )
        return
    else:
        provider = default_provider

    return provider


def init_instrumentations(
    disable_instrumentations: Optional[DisableInstrumentations] | None,
    all_instrumentations: dict,
    tracer_provider: TracerProvider
):
    if disable_instrumentations is None:
        for _, v in all_instrumentations.items():
            v.instrument(tracer_provider=tracer_provider)
    else:

        validate_instrumentations(disable_instrumentations)

        for key in disable_instrumentations:
            for vendor in disable_instrumentations[key]:
                if key == "only":
                    filtered_dict = {
                        k: v
                        for k, v in all_instrumentations.items()
                        if k != vendor.value
                    }
                    for _, v in filtered_dict.items():
                        v.instrument(tracer_provider=tracer_provider)
                else:
                    filtered_dict = {
                        k: v
                        for k, v in all_instrumentations.items()
                        if k == vendor.value
                    }

                    for _, v in filtered_dict.items():
                        v.instrument(tracer_provider=tracer_provider)


def validate_instrumentations(disable_instrumentations):
    if disable_instrumentations is not None:
        for key, value in disable_instrumentations.items():
            if isinstance(value, str):
                # Convert single string to list of enum values
                disable_instrumentations[key] = [InstrumentationType.from_string(value)]
            elif isinstance(value, list):
                # Convert list of strings to list of enum values
                disable_instrumentations[key] = [
                    (
                        InstrumentationType.from_string(item)
                        if isinstance(item, str)
                        else item
                    )
                    for item in value
                ]
            # Validate all items are of enum type
            if not all(
                isinstance(item, InstrumentationType)
                for item in disable_instrumentations[key]
            ):
                raise TypeError(
                    f"All items in {key} must be of type InstrumentationType"
                )
        if (
            disable_instrumentations.get("all_except") is not None
            and disable_instrumentations.get("only") is not None
        ):
            raise ValueError(
                "Cannot specify both only and all_except in disable_instrumentations"
            )


def init_spans_exporter(api_endpoint: str, headers: Dict[str, str]) -> SpanExporter:
    return OTLPJsonSpanExporter(endpoint=f"{api_endpoint}/v1/traces", headers=headers)
