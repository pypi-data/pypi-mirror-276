from abc import ABC, abstractmethod
from typing import Optional

from ..model import Response, Query, Protocol


class BaseProtocol(ABC):
    EXECUTE_ERROR_IGNORE: bool = False

    def __init__(self, protocol: Optional[Protocol] = None):
        self.protocol = protocol

    @abstractmethod
    def connect(self) -> None:
        raise NotImplementedError('Метод connect не реализован')

    @abstractmethod
    def execute(self, query: Query) -> Response:
        raise NotImplementedError('Метод execute не реализован')

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError('Метод close не реализован')
