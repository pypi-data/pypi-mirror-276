from abc import ABC, abstractmethod

from enciyo.model.request import Request


class Interceptor(ABC):
    @abstractmethod
    def process(self, request: Request) -> Request:
        pass
