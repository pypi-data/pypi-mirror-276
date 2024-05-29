from typing import List

from docker import DockerClient

from ambient_edge_server.event_handlers.base_handler import BaseHandler
from ambient_edge_server.event_handlers.deploy_service_handler import (
    DeployServiceHandler,
)
from ambient_edge_server.event_handlers.test_handler import TestHandler
from ambient_edge_server.services.event_service import EventService


class HandlerService:
    def __init__(self, event_service: EventService, docker_client: DockerClient):
        self._handlers: List[BaseHandler] = [
            TestHandler(event_service),
            DeployServiceHandler(event_service, docker_client=docker_client),
        ]

    async def start(self):
        for handler in self._handlers:
            await handler.subscribe()

    def get_handlers(self):
        return self._handlers
