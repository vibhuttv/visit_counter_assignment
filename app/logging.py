import sys
import logging


logger = logging.getLogger("visit-counter")

logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)