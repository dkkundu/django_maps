"""Core > tests > utils.py"""
# PYTHON IMPORTS
import logging


def _suppress_logs(original_function, loglevel=None):
    """If we need to test for 404s or 405s etc, this decorator can prevent the
    request class from throwing warnings and/or errors"""
    if not loglevel:
        loglevel = 'ERROR'

    def new_function(*args, **kwargs):
        """wrap original_function with suppressed warnings"""
        # raise logging level to ERROR or loglevel
        logger = logging.getLogger('django')
        previous_logging_level = logger.getEffectiveLevel()
        logger.setLevel(getattr(logging, loglevel.upper()))

        # trigger original function that would throw warning
        original_function(*args, **kwargs)

        # lower logging level back to previous
        logger.setLevel(previous_logging_level)

    return new_function


def suppress_errors(original_function):
    """Prevent from displaying ERROR logs and below"""
    return _suppress_logs(original_function, loglevel='CRITICAL')


def suppress_warnings(original_function):
    """Prevent from displaying WARNING logs and below"""
    return _suppress_logs(original_function, loglevel='ERROR')


def suppress_infos(original_function):
    """Prevent from displaying INFO logs and below"""
    return _suppress_logs(original_function, loglevel='WARNING')
