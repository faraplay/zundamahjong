import logging
import logging.handlers


def create_server_logger(name: str):
    logger = logging.getLogger(name)

    formatter = logging.Formatter(
        fmt="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt="%d/%b/%Y %H:%M:%S",
    )

    debug_handler = logging.handlers.RotatingFileHandler(
        "server_debug.log", maxBytes=1024 * 1024, backupCount=5, encoding="utf-8"
    )
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(formatter)

    info_handler = logging.handlers.RotatingFileHandler(
        "server_info.log", maxBytes=1024 * 1024, backupCount=5, encoding="utf-8"
    )
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)

    logger.addHandler(debug_handler)
    logger.addHandler(info_handler)


def create_root_logger():
    logger = logging.getLogger()

    formatter = logging.Formatter(
        fmt="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt="%d/%b/%Y %H:%M:%S",
    )

    info_handler = logging.handlers.RotatingFileHandler(
        "info.log", maxBytes=1024 * 1024, backupCount=5, encoding="utf-8"
    )
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)

    logger.addHandler(info_handler)
