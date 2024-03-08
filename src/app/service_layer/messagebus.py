# pylint: disable=broad-except, attribute-defined-outside-init
from __future__ import annotations

import logging
import typing as t

from src.app.domain import commands
from src.app.domain import events

if t.TYPE_CHECKING:
    from src.app.service_layer import unit_of_work

logger = logging.getLogger(__name__)

Message = commands.Command | events.Event


class MessageBus:
    """Handles messages and dispatches them to the appropriate handlers."""

    def __init__(
        self,
        uow: unit_of_work.AbstractUnitOfWork,
        event_handlers: list[t.Type[events.Event], list[t.Callable]],
        command_handlers: t.Dict[t.Type[commands.Command], t.Callable],
    ):
        """Initializes the MessageBus with the given parameters."""
        self.uow = uow
        self.event_handlers = event_handlers
        self.command_handlers = command_handlers

    def handle(self, message: Message):
        """"""
        self.queue = [message]
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, events.Event):
                self.handle_event(message)
            elif isinstance(message, commands.Command):
                self.handle_command(message)
            else:
                raise Exception(f"{message} was not an Event or Command")

    def handle_event(self, event: events.Event):
        """"""
        for handler in self.event_handlers[type(event)]:
            try:
                logger.debug("handling event %s with handler %s", event, handler)
                handler(event)
                self.queue.extend(self.uow.collect_new_events())
            except Exception:
                logger.exception("Exception handling event %s", event)
                continue

    def handle_command(self, command: commands.Command):
        """"""
        logger.debug("handling command %s", command)
        try:
            handler = self.command_handlers[type(command)]
            handler(command)
            self.queue.extend(self.uow.collect_new_events())
        except Exception:
            logger.exception("Exception handling command %s", command)
            raise