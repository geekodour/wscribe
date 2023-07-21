# see https://docs.python.org/3/howto/logging.html
import logging

import structlog

import localsetup  # my custom debug helper
from bake import kitchen


def main():
    localsetup.init()
    L = logging.getLogger(__name__)
    log = structlog.get_logger()
    log.critical("logging from structlog")
    L.info("logging from stdlib log")
    kitchen.do_something()


if __name__ == "__main__":
    main()
