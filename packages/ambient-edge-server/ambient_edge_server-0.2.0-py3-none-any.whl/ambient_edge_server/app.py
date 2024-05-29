from fastapi import FastAPI

from ambient_edge_server.routers import auth, daemon, ping, ports
from ambient_edge_server.services.service_manager import svc_manager
from ambient_edge_server.utils import logger

app = FastAPI()


async def startup():
    logger.info("Starting up ...")
    try:
        await svc_manager.init()
        logger.info("Services initialized.")
    except Exception as e:
        logger.warning("Failed to initialize services: %s", e)


app.add_event_handler("startup", startup)

routers = [ping, ports, auth, daemon]

for router in routers:
    app.include_router(router.router)
