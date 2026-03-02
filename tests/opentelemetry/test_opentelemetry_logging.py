import logging
import pytest
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
    InMemorySpanExporter,
)
from opentelemetry.instrumentation.logging import LoggingInstrumentor

# Configure opentelemetry
trace.set_tracer_provider(TracerProvider())
span_exporter = InMemorySpanExporter()
trace.get_tracer_provider().add_span_processor(
    SimpleSpanProcessor(span_exporter)
)
LoggingInstrumentor(set_logging_format=True)

# Configure logger to use opentelemetry trace ids
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

@pytest.fixture(scope="session", autouse=True)
def cleanup():
    yield
    # Clean up after the test
    trace.get_tracer_provider().shutdown()

def test_logging_with_span():
    with trace.get_tracer(__name__).start_as_current_span("test_span"):
        logger.info("This is a logged message within a span")

    spans = span_exporter.get_finished_spans()
    assert len(spans) == 1
    assert spans[0].name == "test_span"
    assert "span_id" in spans[0].attributes
    assert "trace_id" in spans[0].attributes

if __name__ == "__main__":
    pytest.main([__file__])
