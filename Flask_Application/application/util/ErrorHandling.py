from application import logger
from flask import Response
import traceback
# Decorators
def exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            if res:
                return res
            else:
                return Response(status=200)
            # if func(*args, **kwargs):
            #     return func(*args, **kwargs)
            # else:
            #     return Response(status=200)
        except Exception as e:
            # Log error message
            logger.error(f" The function {func.__name__} failed with the error: {e}")
            # Log full traceback
            logger.error(traceback.format_exc())
            return Response(status=422)
    return inner_function
