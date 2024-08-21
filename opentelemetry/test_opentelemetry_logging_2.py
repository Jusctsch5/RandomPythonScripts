import logging
import pytest
from opentelemetry import trace
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
    InMemorySpanExporter,
)

# logging.basicConfig(level=logging.INFO)  # Set log level to INFO

@pytest.fixture
def setup_opentelemetry():
    trace.set_tracer_provider(TracerProvider())
    span_exporter = InMemorySpanExporter()
    trace.get_tracer_provider().add_span_processor(
        SimpleSpanProcessor(span_exporter)
    )
    instrumenter = LoggingInstrumentor(logging_format='%(msg)s [span_id=%(span_id)s]')
    instrumenter.instrument()

    # LoggingInstrumentor(set_logging_format=True, log_level=logging.INFO).instrument()


@pytest.fixture
def create_span():
    # Create a span for testing
    with trace.get_tracer_provider().get_tracer(__name__).start_as_current_span("test_span"):
        yield

def test_opentelemetry_logging(setup_opentelemetry, create_span):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    # Log a message within the span
    logger.error("Test message")
    logging.error("Test message")

