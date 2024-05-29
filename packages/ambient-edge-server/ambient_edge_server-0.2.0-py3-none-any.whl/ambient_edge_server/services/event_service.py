import asyncio
from abc import ABC, abstractmethod
from typing import Callable, Set, Union

from ambient_backend_api_client import EventLabel
from ambient_event_bus_client import Client, Message, MessageCreate
from result import Err, Result

from ambient_edge_server.repos.node_repo import NodeRepo
from ambient_edge_server.utils import logger


class EventService(ABC):
    @abstractmethod
    async def start(self) -> None:
        """Start the event service."""

    @abstractmethod
    async def stop(self) -> None:
        """Stop the event service."""

    @abstractmethod
    async def add_event_handler(
        self, event_label: EventLabel, handler: Callable
    ) -> None:
        """Add an event handler to the event service.

        Args:
            event_label (EventLabel): Event label
            handler (Callable): async function to handle the event
        """

    @abstractmethod
    async def send_event(self, topic: str, msg: str) -> None:
        """Send an event to the event service.

        Args:
            event (Event): Event to send
        """

    @property
    @abstractmethod
    async def is_running(self) -> bool:
        """Check if the event service is running.

        Returns:
            bool: True if the event service is running, False otherwise
        """

    @property
    @abstractmethod
    def error(self) -> Union[Result, None]:
        """Get the current error state of the event service.

        Returns:
            Result: The current error state
        """


class AmbientBusEventService(EventService):
    def __init__(self, client: Client, node_repo: NodeRepo) -> None:
        self.client = client
        self.node_repo = node_repo
        self.handlers = {}
        self.tasks: Set[asyncio.Task] = set()
        self._error = None
        self._is_connected = False

    async def start(self) -> None:
        logger.info("Starting event service ...")
        await self.client.init_client()
        node = self.node_repo.get_node_data()
        if node:
            await self.client.add_subscription(f"node-{node.id}/*")
        logger.debug("event client initialized.")

        logger.info("Starting subscription loop ...")
        sub_loop_task = asyncio.create_task(self._subscription_loop())
        sub_loop_task.add_done_callback(self._done_callback)
        sub_loop_task.set_name("subscription_loop_task")
        self.tasks.add(sub_loop_task)
        logger.info("subscription loop started.")

    async def stop(self) -> None:
        logger.info("Stopping event service ...")
        for task in self.tasks:
            logger.debug("cancelling task: %s", task.get_name())
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

    async def add_event_handler(
        self, event_label: EventLabel, handler: Callable
    ) -> None:
        logger.info("Adding event handler for event: %s", event_label.value)

        logger.debug(
            "handler name: %s [ from %s ]", handler.__name__, handler.__module__
        )
        self.handlers[event_label.value] = handler

    async def send_event(self, topic: str, msg: str) -> None:
        message_data = MessageCreate(topic=topic, message=msg)
        logger.debug("Publishing message:\n%s", message_data.model_dump_json(indent=4))
        await self.client.publish(msg)

    @property
    async def is_running(self) -> bool:
        return all(task.done() for task in self.tasks) and self._is_connected

    @property
    def error(self) -> Union[Err, None]:
        return self._error

    async def _get_handler(self, topic: str) -> Callable:
        logger.debug("Getting handler for topic: %s", topic)
        handler_items = self.handlers.items()
        logger.debug("handlers: %s", handler_items)
        for event_label, handler in handler_items:
            if event_label in topic:
                logger.debug("Handler found for topic: %s", topic)
                return handler
        logger.info("No handler found for topic: %s", topic)
        return None

    async def _handle_event(self, msg: Message) -> None:
        handler = await self._get_handler(msg.topic)
        if handler:
            try:
                await handler(msg)
            except Exception as e:
                self._error = Err(e)
        else:
            self._error = Err(f"No handler for event: {msg.topic}")

    async def _subscription_loop(self) -> None:
        logger.info("Starting subscription loop ...")
        while True:
            self._error = None
            self._is_connected = True
            try:
                async for message in self.client.subscribe():
                    logger.debug(
                        "Received message:\n%s", message.model_dump_json(indent=4)
                    )
                    await self._handle_event(message)
            except Exception as e:
                self._error = Err(e)

    async def _done_callback(self, task: asyncio.Task) -> None:
        err_msg = f"task {task.get_name()} ended. \
Result: {task.result() if task.done() else task.exception()}"
        logger.warning(err_msg)
        self._error = Err(err_msg)

        logger.debug("removing task from tasks set ...")
        self.tasks.remove(task)

        logger.info("restarting subscription loop ...")
        sub_loop_task = asyncio.create_task(self._subscription_loop())
        sub_loop_task.add_done_callback(self._done_callback)
        sub_loop_task.set_name("subscription_loop_task")
        self.tasks.add(sub_loop_task)
        logger.info("subscription loop restarted.")
