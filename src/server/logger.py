import logging

# logging.basicConfig(filename="server.log", encoding="utf-8", level=logging.INFO)

logger = logging.getLogger()

formatter = logging.Formatter(
    fmt="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
    datefmt="%d/%b/%Y %H:%M:%S",
)

debug_handler = logging.FileHandler("debug.log", encoding="utf-8")
debug_handler.setLevel(logging.DEBUG)
debug_handler.setFormatter(formatter)

info_handler = logging.FileHandler("server.log", encoding="utf-8")
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(formatter)

logger.addHandler(debug_handler)
logger.addHandler(info_handler)
