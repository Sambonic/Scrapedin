from src.config.common_imports import psutil,functools,time
from src.managers.logger_manager import logger

def benchmark(func):
    """Decorator to measure time and space complexity of a function."""
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        start_time = time.time()
        process = psutil.Process()
        memory_before = process.memory_info().rss

        result = func(self, *args, **kwargs)

        end_time = time.time()
        memory_after = process.memory_info().rss

        execution_time = end_time - start_time
        memory_usage = abs(memory_before - memory_after)

        logger.info(f"Function '{func.__name__}' execution time: {execution_time:.4f} seconds")
        logger.info(f"Memory usage change: {memory_usage} bytes")

        return result

    return wrapper
