import logging
import logging.handlers
import sys
import time

import os

logger = logging.getLogger(__name__)


def logging_config(name):
    if not os.path.exists('log'):
        os.mkdir('log')
    base = os.path.join('log', name + '_' + time.strftime('%Y%m%d_%H%M%S'))
    log_filename = base + '.log'
    log_running = name + '_running.log'
    c_handler = logging.StreamHandler()
    f_handler = logging.handlers.RotatingFileHandler(log_filename)
    r_handler = logging.handlers.RotatingFileHandler(log_running, mode='w')

    c_handler.setLevel(logging.INFO)
    f_handler.setLevel(logging.INFO)
    r_handler.setLevel(logging.INFO)
    # Create formatters and add it to handlers
    c_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)5s - %(module)s.%(funcName)s():%(lineno)d - %(message)s')
    f_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)5s - %(module)s.%(funcName)s():%(lineno)d - %(message)s')

    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)
    r_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
    logger.addHandler(r_handler)
    logger.setLevel(logging.INFO)

    # Redirect the system exception to log - error
    sys.stderr = open(base + '_exception.log', 'w')
    sys.stdout = open(base + '_info.log', 'w')
