import os
import logging

from pathlib import Path

from .version import __version__


PATH_ENVIRON = "PATH"
logger = logging.getLogger(__name__)


def check_jdk_environ_variable(exe_name: str) -> bool:
    """
    Check if executable needed in jdk is available
    """
    path_list = os.environ[PATH_ENVIRON].split(';')
    for path in path_list:
        if os.path.isfile(Path(path) / exe_name):
            return True

    logger.error("Java Error: jdk_create_jar: no jdk set up in PATH environment variable, "
                 "please download JAVA JDK and add it to PATH")
    return False


def init_logging(log_path: str, verbose: bool = False) -> logging.Logger:
    # Create logger.
    logging.basicConfig(filename=log_path, level=logging.DEBUG, filemode='w', format='%(asctime)s | %(message)s')
    logger = logging.getLogger()
    ch = logging.StreamHandler()
    if verbose:
        # Log to console also.
        ch.setLevel(logging.DEBUG)
    else:
        ch.setLevel(logging.INFO)
    logger.addHandler(ch)

    logger.debug("Starting Tableau Connector Packaging Version " + __version__)

    return logger
