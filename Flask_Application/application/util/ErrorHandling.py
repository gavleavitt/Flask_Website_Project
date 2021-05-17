from application import logger
from flask import Response
import traceback
# Decorators
def exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Log error message
            logger.error(f" The function {func.__name__} failed with the error: {e}")
            # Log full traceback
            logger.error(traceback.format_exc())
            return Response(status=500)
    return inner_function
