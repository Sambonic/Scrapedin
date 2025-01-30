from src.configurations.common_imports import functools

def log_function_call(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            result = func(self, *args, **kwargs)
            if hasattr(self, 'logger'):
                self.logger.info(f"Successfully executed {func.__name__}.")
            return result
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.error(f"Error in {func.__name__}: {e}")
            raise
    return wrapper

