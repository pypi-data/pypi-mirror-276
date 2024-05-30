import os

from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SimpleSpanProcessor, ConsoleSpanExporter
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
        BatchSpanProcessor,
        ConsoleSpanExporter,
    )

from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.trace import Status, StatusCode
from opentelemetry.instrumentation.flask import FlaskInstrumentor


def FlaskInstrument(service_name, app, infrastackai_api_key=None):
    if infrastackai_api_key is None:
        infrastackai_api_key = os.getenv("INFRASTACKAI_API_KEY")
    if not infrastackai_api_key:
        raise ValueError("infrastackai_api_key is required")


    resource = Resource.create({"service.name": service_name})
    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)



    # Adds span processor with the OTLP exporter to the tracer provider
    provider.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter(endpoint="https://collector-us1-http.infrastack.ai/v1/traces", headers=(("infrastack-api-key", infrastackai_api_key),)))
    )

    FlaskInstrumentor().instrument_app(app, tracer_provider=provider)

