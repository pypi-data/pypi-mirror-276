import logging

from ambient_edge_server.config import settings

logger = logging.getLogger("ambient_edge_server")
# load basic configuration
logging.basicConfig()
logger.setLevel(settings.ambient_log_level)
