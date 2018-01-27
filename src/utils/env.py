import os
import logging


def get_optional_env(key, default):
    """
    Return the value of an optional environment variable, and use
    the provided default if it's not set.

    Arguments keywords:
    key -- Name of variable we want to get the value
    default -- Value to return if 'key' not found in environment variables
    """
    if not os.environ.get(key):
        logging.warning(
            "The optional environment variable {} is not set, using '{}' as default".format(key, default))

    return os.environ.get(key, default)


def get_mandatory_env(key):
    """
    Return the value of a mandatory environment variable. If the variable doesn't exists, exception is raised.

    Arguments keywords:
    key -- Name of mandatory variable we want to get the value
    """
    if not os.environ.get(key):
        msg = "The mandatory environment variable {} is not set".format(key)
        logging.error(msg)
        raise Exception(msg)

    return os.environ.get(key)
