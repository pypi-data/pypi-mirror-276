from ambient_backend_api_client import EventLabel
from ambient_event_bus_client import Message

from ambient_edge_server.event_handlers.base_handler import BaseHandler
from ambient_edge_server.services.event_service import EventService
from ambient_edge_server.utils import logger


class TestHandler(BaseHandler):
    def __init__(self, event_service: EventService):
        super().__init__(event_service)

    async def handle(self, msg: Message) -> None:
        logger.debug("Handling test msg: %s", msg.model_dump_json(indent=4))

    @property
    def label(self) -> EventLabel:
        return EventLabel.TEST_LABEL
