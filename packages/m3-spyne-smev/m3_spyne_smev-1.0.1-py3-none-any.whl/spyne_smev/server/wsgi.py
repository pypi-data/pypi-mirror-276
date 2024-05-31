from spyne.server.wsgi import WsgiApplication as _SpyneWsgiApplication

from spyne_smev.server import _AllYourInterfaceDocuments


class WsgiApplication(_SpyneWsgiApplication):

    # pylint: disable=abstract-method

    def __init__(self, app, chunked=True, max_content_length=2 * 1024 * 1024,
                 block_length=8 * 1024):
        super(WsgiApplication, self).__init__(app, chunked, max_content_length,
                                              block_length)

        self.app.interface.docs = _AllYourInterfaceDocuments(app.interface)
