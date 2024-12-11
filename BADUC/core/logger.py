import logging
from logging.handlers import RotatingFileHandler

# Setup Logging
logging.basicConfig(
    format="[%(name)s]:: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
    handlers=[
        RotatingFileHandler("logs.txt", maxBytes=(1024 * 1024 * 5), backupCount=10),
        logging.StreamHandler(),
    ],
)

# Suppress noisy loggers
for module in ["apscheduler", "asyncio", "httpx", "pyrogram", "pytgcalls"]:
    logging.getLogger(module).setLevel(logging.ERROR)

LOGGER = logging.getLogger("SYSTEM")
