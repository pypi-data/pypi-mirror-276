import json
from typing import Any, Dict

import docker
import websockets
from ambient_backend_api_client import EventLabel, Service
from ambient_event_bus_client import Message
from result import Err, Ok, Result

from ambient_edge_server.event_handlers.base_handler import BaseHandler
from ambient_edge_server.services.event_service import EventService
from ambient_edge_server.utils import logger


class DeployServiceHandler(BaseHandler):
    def __init__(
        self, event_service: EventService, docker_client: docker.DockerClient
    ) -> None:
        super().__init__(event_service)
        self.docker_client = docker_client

    async def handle(self, msg: Message) -> None:
        logger.info("Handling deploy service msg: %s", msg.topic)
        logger.debug(msg.model_dump_json(indent=4))

        ws_session_data: Dict[str, Any] = json.loads(msg.message)
        ws_session = ws_session_data.get("ws_session")
        logger.debug("ws_session: %s", ws_session)

        logger.info("connecting to ws session %s ...", ws_session)

        try:
            async with websockets.connect(ws_session) as ws:
                try:
                    logger.info("connected to ws session %s", ws_session)
                    await ws.send("ack")
                    logger.debug("ack sent")

                    service_spec_str = await ws.recv()
                    logger.debug("Received service spec: %s", service_spec_str)

                    service = Service.model_validate_json(service_spec_str)
                    logger.debug(
                        "parsed service spec: %s", service.model_dump_json(indent=4)
                    )

                    logger.info("deploying service %s ...", service.name)
                    result = await self.__deploy_service(service)

                    if result.is_ok():
                        logger.info("service %s deployed", service.name)
                        await ws.send("deployed")
                        return
                    logger.error("error deploying service %s", service.name)
                    await ws.send(f"error: {result.unwrap_err()}")
                except Exception as e:
                    logger.error("Error deploying service: %s", e)
                    await ws.send(f"error: {str(e)}")
        except Exception as e:
            logger.error("Error connecting to ws session: %s", e)

    async def __deploy_service(self, service: Service) -> Result[None, str]:
        """Deploy a service using the docker client

        Args:
            service (Service): Service to deploy

        Returns:
            Result[None, str]: Result of the deployment
        """
        try:
            self.docker_client.services.create(
                image=service.image,
                name=service.name,
            )
            return Ok(None)
        except Exception as e:
            logger.error("Error deploying service %s: %s", service.name, e)
            return Err(str(e))

    @property
    def label(self) -> EventLabel:
        return EventLabel.SERVICE_DEPLOYMENT_REQUESTED
