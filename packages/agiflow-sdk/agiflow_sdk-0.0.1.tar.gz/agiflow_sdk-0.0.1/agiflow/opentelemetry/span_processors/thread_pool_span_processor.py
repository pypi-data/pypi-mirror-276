import logging
import typing

from opentelemetry.sdk.trace import SpanProcessor, ReadableSpan, Span
from opentelemetry.sdk.trace.export import SpanExporter
from opentelemetry.context import (
    _SUPPRESS_INSTRUMENTATION_KEY,
    Context,
    attach,
    detach,
    set_value,
)
from collections import deque
from multiprocessing.dummy import Pool
import atexit


class ThreadPoolSpanProcessor(SpanProcessor):
    """InMemory SpanProcessor implementation.

    InMemorySpanProcessor is an implementation of `SpanProcessor` that
    send remote request using threadpool instead of long-running thread.
    """

    def __init__(
        self,
        span_exporter: SpanExporter,
        max_queue_size=10,
        pool_size=4,
        pool_queue_size=10
    ):
        self.pool = Pool(pool_size)
        self.max_queue_size = max_queue_size
        self.futures = deque([], pool_queue_size)
        self.span_exporter = span_exporter
        self.queue = []
        try:
            atexit.register(self.wait_for_flush)
        except Exception as e:
            logging.warn(e)

    def on_start(
        self,
        span: Span,
        parent_context: typing.Optional[Context] = None
    ) -> None:
        pass

    def on_end(self, span: ReadableSpan) -> None:
        token = attach(set_value(_SUPPRESS_INSTRUMENTATION_KEY, True))
        self.queue.append(span)
        if len(self.queue) == self.max_queue_size:
            self.futures.append(self.pool.apply_async(self._export, self.queue))
            self.queue = []
        detach(token)

    def shutdown(self) -> None:
        self.span_exporter.shutdown()

    def _export(self, *seq):
        self.span_exporter.export(seq)

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        if len(self.queue) != 0:
            self.futures.append(self.pool.apply_async(self._export, self.queue))
            self.queue = []
        # pylint: disable=unused-argument
        return True

    def wait_for_flush(self):
        try:
            for future in self.futures:
                logging.info(future.get())
        except Exception as e:
            logging.error(e)

        self.futures = []
