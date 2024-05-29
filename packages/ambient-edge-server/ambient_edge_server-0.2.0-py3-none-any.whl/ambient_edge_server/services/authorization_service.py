from typing import Union

import aiohttp
from ambient_backend_api_client import (
    ApiClient,
    Configuration,
    Node,
    NodesApi,
    PingApi,
    TokenResponse,
)
from async_lru import alru_cache
from result import Err, Ok, Result

from ambient_edge_server.config import settings
from ambient_edge_server.repos.node_repo import NodeRepo
from ambient_edge_server.repos.token_repo import TokenRepository
from ambient_edge_server.utils import logger


class AuthorizationService:
    def __init__(self, token_repo: TokenRepository, node_repo: NodeRepo) -> None:
        self.token_repo = token_repo
        self.node_repo = node_repo
        self._node_id = None

    @alru_cache(maxsize=1, ttl=3600)
    async def get_token(self) -> Union[str, None]:
        logger.debug("node_id: %s", self.node_id)
        if not self.node_id:
            result = await self.fetch_node()
            logger.debug("result: %s", result)
            if result.is_err():
                logger.error("Error fetching node: %s", result.unwrap_err())
                return None
            self.node_id = result.unwrap().id
        await self.refresh_token()
        return self.token_repo.get_access_token()

    async def verify_authorization_status(self) -> Result[str, str]:
        if not self.token_repo.get_access_token():
            return Err("Unauthorized")
        return await self.test_authorization()

    async def fetch_node(self, refresh: bool = False) -> Result[Node, str]:
        if not refresh:
            node = self.node_repo.get_node_data()
            if node:
                logger.debug("node: %s", node.model_dump_json(indent=4))
                return Ok(node)
        node_id = self.node_repo.get_node_id()
        if not node_id:
            return Err("Node not found")
        logger.info("fetching node %d ...", node_id)
        try:
            async with ApiClient(self.api_config) as api_client:
                nodes_api = NodesApi(api_client)
                logger.debug("node_id: %s", node_id)
                if not node_id:
                    return Err("Node ID not found")
                node = await nodes_api.get_node_nodes_node_id_get(node_id=int(node_id))
                logger.debug("node: %s", node.model_dump_json(indent=4))
                self.node_repo.save_node_data(node=node)
                self.node_id = node.id
                return Ok(node)
        except Exception as e:
            err_msg = f"Error fetching node: {e}"
            logger.error(err_msg)
            return Err(err_msg)

    async def authorize_node(self, node_id: str, device_code: str) -> None:
        self.node_id = node_id
        async with aiohttp.ClientSession() as session:
            url = settings.backend_api_url
            id = node_id
            code = device_code
            async with session.post(
                f"{url}/nodes/{id}/authorize?device_code={code}"
            ) as response:
                response.raise_for_status()
                token_response = TokenResponse.model_validate(await response.json())
                logger.debug(
                    "token_response: %s", token_response.model_dump_json(indent=4)
                )
                self.token_repo.save_access_token(token_response.access_token)
                self.token_repo.save_refresh_token(token_response.refresh_token)

        await self.get_and_save_node_data(node_id=int(node_id))

    async def get_and_save_node_data(self, node_id: int) -> Result[Node, str]:
        logger.info("fetching node %d ...", node_id)
        try:
            async with aiohttp.ClientSession() as session:
                url = settings.backend_api_url
                async with session.get(f"{url}/nodes/{node_id}") as response:
                    response.raise_for_status()
                    node = Node.model_validate(await response.json())
                    logger.debug("node: %s", node.model_dump_json(indent=4))
                    self.node_repo.save_node_data(node=node)
                    self.node_id = node.id
                    return Ok(node)
        except Exception as e:
            err_msg = f"Error fetching node: {e}"
            logger.error(err_msg)
            return Err(err_msg)

    async def refresh_token(self) -> None:
        logger.info("refreshing token ...")
        async with ApiClient(self.api_config) as api_client:
            nodes_api = NodesApi(api_client)
            logger.debug("refresh_token: %s", self.token_repo.get_refresh_token())
            logger.debug("node_id: %s", self.node_id)
            token_resp = (
                await nodes_api.refresh_node_token_nodes_node_id_refresh_token_post(
                    node_id=self.node_id,
                    refresh_token=self.token_repo.get_refresh_token(),
                )
            )
            logger.debug("token_resp: %s", token_resp.model_dump_json(indent=4))
            self.token_repo.save_access_token(token_resp.access_token)

    async def test_authorization(self) -> Result[str, str]:
        try:
            async with ApiClient(self.api_config) as api_client:
                ping_api = PingApi(api_client)
                pong = await ping_api.auth_ping_auth_ping_get()
                logger.debug("pong: %s", pong)
                return Ok("Authorized")
        except Exception as e:
            logger.error("Error: %s", e)
            return Err("Unauthorized")

    @property
    def node_id(self) -> str:
        return self._node_id

    @node_id.setter
    def node_id(self, value: str) -> None:
        self._node_id = value

    @property
    def api_config(self) -> Configuration:
        return Configuration(
            host=settings.backend_api_url,
            access_token=self.token_repo.get_access_token(),
        )
