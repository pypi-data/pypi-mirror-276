from ussl.model import Protocol
from ussl.protocol.base import BaseProtocol


class WMIProtocol(BaseProtocol):
    name = 'wmi'

    def connect(
        self,
        protocol: Protocol,
    ):
        pass

    def close(self):
        pass

    def execute(self, query):
        pass