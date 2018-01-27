import logging


def set_logging_config(kwargs):
    """
    Set logging with the 'good' level

    Arguments keywords:
    kwargs -- list containing parameters passed to script
    """
    # set up level of logging
    level = logging.INFO
    if kwargs['--quiet']:
        level = logging.WARNING
    elif kwargs['--debug']:
        level = logging.DEBUG

    # set up logging to console
    logging.basicConfig(format='%(levelname)s - %(funcName)s - %(message)s')
    logger = logging.getLogger()
    logger.setLevel(level)
