from traceback import format_exc
import logging

from spyne.application import Application as SpyneApplication
from spyne.error import InternalError
from spyne.model.fault import Fault


logger = logging.getLogger(__name__)


class Application(SpyneApplication):
    """
    Замена Application из spyne. Позволяет дополнительно обрабатывать эксепшны

    файрит ивент, method_call_exception, но в аргументе передает не контекст,
    а форматированный текст exception
    """

    def call_wrapper(self, ctx):
        try:
            return super(Application, self).call_wrapper(ctx)
        except Fault as e:
            logger.exception(e)
            raise
        except Exception as e:
            e_text = format_exc()
            self.event_manager.fire_event("method_call_exception", e_text)
            logger.exception(e)
            raise InternalError(e)
