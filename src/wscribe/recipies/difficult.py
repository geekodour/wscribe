import structlog

LOGGER = structlog.get_logger()
LOGGER = LOGGER.bind(user_agent="ff", peer_ip="1.1.1.1")


def hard_stuff():
    LOGGER.info("logging hard stuff")
    return "hard stuff"
