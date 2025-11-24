import time
import uuid
from functools import wraps
from .logger import get_logger

logger = get_logger("Tracer")

def trace_span(name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            span_id = str(uuid.uuid4())[:8]
            start_time = time.time()
            logger.info(f"Trace [{span_id}] STARTED: {name}")
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                logger.info(f"Trace [{span_id}] COMPLETED: {name} in {duration:.2f}s")
                return result
            except Exception as e:
                logger.error(f"Trace [{span_id}] FAILED: {name} - {str(e)}")
                raise e
        return wrapper
    return decorator