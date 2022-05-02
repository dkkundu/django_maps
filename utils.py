"""DJMAPS > utils.py"""
# PYTHON IMPORTS
import logging
from sys import _getframe

# do not import any app related stuff here
# for specific app utils, please create utils.py in your app directory
# functions here will be used project-wide, may be in multiples apps

logger = logging.getLogger(__name__)


def test_user(user, allow_staff=True, allow_other=False):
    """Tests user if is_active, is_staff, is_superuser
    Returns boolean status, True/False"""
    if user.is_active:
        if user.is_superuser:
            logger.debug(  # prints class and function name
                f"{_getframe().f_code.co_name} {user} is a superuser."
            )
            return True
        elif user.is_staff and allow_staff:
            logger.debug(  # prints class and function name
                f"{_getframe().f_code.co_name} {user} is a staff."
            )
            return True
        else:  # test for other
            logger.debug(  # prints class and function name
                f"{_getframe().f_code.co_name} {user} is a other."
            )
            return allow_other

    # user not active
    logger.debug(  # prints class and function name
        f"{_getframe().f_code.co_name} {user} is not active."
    )
    return False
