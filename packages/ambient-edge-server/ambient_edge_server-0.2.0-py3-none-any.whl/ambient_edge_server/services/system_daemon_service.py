import getpass
import grp
import os
import pwd
import subprocess
from abc import ABC, abstractmethod
from typing import Optional, Union

from result import Err, Ok, Result

from ambient_edge_server.models.system_service import (
    ServiceConfigBase,
    ServiceConfigLinux,
)
from ambient_edge_server.repos.system_daemon_repo import SystemDaemonRepo
from ambient_edge_server.utils import logger


class SystemDaemonService(ABC):
    @abstractmethod
    async def install(self) -> Union[None, Err[str]]:
        """Initialize the service."""

    @abstractmethod
    async def save_config(self) -> Result[str, str]:
        """Save the service to the system."""

    @abstractmethod
    async def start(self) -> Result[str, str]:
        """Start the service."""

    @abstractmethod
    async def stop(self) -> Result[str, str]:
        """Stop the service."""

    @abstractmethod
    async def restart(self) -> Result[str, str]:
        """Restart the service."""

    @property
    @abstractmethod
    def status(self) -> Result[str, str]:
        """Get the status of the service.

        Returns:
            Result[str, str]: The status of the service.
                Ok if the service is running.
                Err if the service is not running.
        """

    @property
    @abstractmethod
    def service_config(self) -> ServiceConfigBase:
        """Return the service configuration."""


class LinuxDaemonService(SystemDaemonService):
    def __init__(self, system_daemon_repo: SystemDaemonRepo):
        self.system_daemon_repo = system_daemon_repo
        self._service_config: ServiceConfigLinux = self.build_service_config()

    async def install(self) -> Optional[Err[str]]:
        """
        This should only be called once when the service is first installed
        on the system. It will render the service configuration and save it to
        the system. It exits upon completion.
        """

        logger.info("starting the installation process ...")
        save_config_result = await self.save_config()
        if save_config_result.is_err():
            logger.error(
                "Failed to save the configuration: %s", save_config_result.err()
            )
            return Err(save_config_result.err())
        else:
            logger.info("Configuration saved successfully.")

        start_result = await self.start()
        if start_result.is_err():
            logger.error("Failed to start the service: %s", start_result.err())
            return start_result
        else:
            logger.info("Service started successfully.")

        logger.info("Installation complete. Exiting ...")
        exit(0)

    @property
    def service_config(self) -> ServiceConfigLinux:
        return self._service_config

    async def save_config(self) -> Result[str, str]:
        logger.info("Saving configuration ...")
        logger.debug("service config: %s", self.service_config)

        result: Result = await self.system_daemon_repo.render_template_and_save(
            self.service_config
        )
        if result.is_err():
            logger.error("Failed to save the configuration: %s", result.err())
            return result
        elif result.is_ok():
            logger.info("Configuration saved successfully.")
            return result

    async def start(self) -> Result[str, str]:
        logger.info("Starting the service ...")

        refresh_result = await self._refresh_services()
        if refresh_result.is_err():
            return refresh_result

        return await self._start_service()

    async def stop(self) -> Result[str, str]:
        return await self._run_systemctl_cmd("stop")

    async def restart(self) -> Result[str, str]:
        return await self._run_systemctl_cmd("restart")

    @property
    def status(self) -> Result[str, str]:
        cmd = ["systemctl", "status", "ambient_edge_server.service"]

        logger.debug("command: %s", cmd)

        try:
            output = subprocess.run(cmd, capture_output=True, text=True)
            logger.debug("output: %s", output)
            output.check_returncode()
            logger.info("service is running.")
            return Ok("service is running.")
        except subprocess.CalledProcessError as e:
            logger.error("service is not running: %s", e)
            return Err("service is not running.")

    async def _refresh_services(self) -> Result[str, str]:
        refresh_cmd = ["systemctl", "daemon-reload"]

        logger.debug("refreshing services ...")
        logger.debug("cmd: %s", refresh_cmd)

        try:
            output = subprocess.run(refresh_cmd, capture_output=True, text=True)
            logger.debug("output: %s", output)
            output.check_returncode()
            logger.info("services refreshed successfully.")
            return Ok("services refreshed successfully.")
        except subprocess.CalledProcessError as e:
            logger.error("Failed to refresh services: %s", e)
            return Err("Failed to refresh services.")

    async def _start_service(self) -> Result[str, str]:
        return await self._run_systemctl_cmd("start")

    async def _run_systemctl_cmd(self, action: str) -> Result[str, str]:

        cmd = ["systemctl", action, "ambient_edge_server.service"]

        logger.debug("command: %s", cmd)

        try:
            output = subprocess.run(cmd, capture_output=True, text=True)
            logger.debug("output: %s", output)
            output.check_returncode()
            logger.info("action %s completed successfully.", action)
            return Ok("action %s completed successfully.", action)
        except subprocess.CalledProcessError as e:
            logger.error("Failed to complete action: %s", e)
            return Err("Failed to complete action.")

    def build_service_config(self) -> ServiceConfigLinux:
        logger.debug("building the service configuration ...")
        user = self.get_user()
        group = self.get_group()
        return ServiceConfigLinux(user=user, group=group)

    def get_user(self) -> str:
        logger.debug("getting the current user ...")
        username = getpass.getuser()
        logger.info("current user: %s", username)
        return username

    def get_group(self) -> str:
        logger.debug("getting the current group ...")

        uid = os.getuid()
        user_info = pwd.getpwuid(uid)
        primary_gid = user_info.pw_gid

        logger.debug(
            "-> uid: %s\n-> primary_gid: %s\n-> user_info: %s",
            uid,
            primary_gid,
            user_info,
        )

        group_info = grp.getgrgid(primary_gid)
        group_name = group_info.gr_name

        logger.info("current group: %s", group_name)
        logger.debug("-> group_info: %s", group_info)

        return group_name
