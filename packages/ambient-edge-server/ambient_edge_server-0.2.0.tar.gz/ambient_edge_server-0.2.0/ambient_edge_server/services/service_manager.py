from ambient_event_bus_client import Client, ClientOptions
from docker import DockerClient

from ambient_edge_server.config import settings
from ambient_edge_server.repos.node_repo import FileNodeRepo
from ambient_edge_server.repos.system_daemon_repo import LinuxSystemDaemonRepo
from ambient_edge_server.repos.token_repo import EncryptedTokenRepository
from ambient_edge_server.services import (
    authorization_service,
    event_service,
    handler_service,
    port_service,
)
from ambient_edge_server.services.system_daemon_service import LinuxDaemonService
from ambient_edge_server.utils import logger


class ServiceManager:
    def __init__(self):
        if settings.platform == "linux":
            self._system_daemon_repo = LinuxSystemDaemonRepo()
            self._system_daemon_service = LinuxDaemonService(self._system_daemon_repo)
        else:
            logger.fatal("Platform not supported")
            raise NotImplementedError("Platform not supported")
        self._port_service = port_service.PortService()
        self._token_repo = EncryptedTokenRepository()
        self._node_repo = FileNodeRepo()
        self._authorization_service = authorization_service.AuthorizationService(
            token_repo=self._token_repo, node_repo=self._node_repo
        )

        self._event_client = Client(
            ClientOptions(
                event_api_url=settings.event_bus_api,
                connection_service_url=settings.connection_service_url,
                api_token="dummy_token",
                log_level="DEBUG",
            )
        )
        self._event_service = event_service.AmbientBusEventService(
            client=self._event_client, node_repo=self._node_repo
        )

        self._docker_client = DockerClient()
        self._handler_service = handler_service.HandlerService(
            self._event_service, docker_client=self._docker_client
        )

    async def init(self):
        await self._port_service.init()

        token = await self._authorization_service.get_token()
        if not token:
            logger.error("Failed to get token")
            return
        logger.debug("got token [ %d chars ]", len(token))
        self._event_client.token = token
        await self._event_client.init_client()
        await self._event_service.start()

        await self._handler_service.start()

    def get_port_service(self):
        return self._port_service

    def get_authorization_service(self):
        return self._authorization_service

    def get_event_service(self):
        return self._event_service

    def get_system_daemon_service(self):
        return self._system_daemon_service


svc_manager = ServiceManager()
