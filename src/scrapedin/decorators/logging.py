from scrapedin.config.common_imports import functools
from scrapedin.managers.logger_manager import logger

def log_function_call(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            result = func(self, *args, **kwargs)
            logger.info(f"Successfully {func.__name__}.".replace('_',' ').replace('  ',' '))
            return result
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            raise
    return wrapper

