import logging
import os

import pandas as pd


def gen_abspath(directory: str, rel_path: str) -> str:
    """
    Generate the absolute path by combining the given directory with a relative path.

    :param directory: The specified directory, which can be either an absolute or a relative path.
    :param rel_path: The relative path with respect to the 'dir'.
    :return: The resulting absolute path formed by concatenating the absolute directory
             and the relative path.
    """
    abs_dir = os.path.abspath(directory)
    return os.path.join(abs_dir, rel_path)


def read_csv(
    file_path: str,
    sep: str = ',',
    header: int = 0,
    on_bad_lines: str = 'warn',
    encoding: str = 'utf-8',
    dtype: dict = None
) -> pd.DataFrame:
    """
    Read a CSV file from the specified path.
    """
    return pd.read_csv(file_path,
                       header=header,
                       sep=sep,
                       on_bad_lines=on_bad_lines,
                       encoding=encoding,
                       dtype=dtype)


def set_logger(name: str, level: int = logging.WARNING):
    """
    Set up the logger for the application.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Create stream_handler and set level
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)

    # Create formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s %(levelname)s [%(name)s]: '
            '(%(module)s:%(funcName)s(%(lineno)d)) - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    stream_handler.setFormatter(formatter)  # add formatter to stream_handler

    # add stream_handler to logger
    logger.addHandler(stream_handler)

    return logger
