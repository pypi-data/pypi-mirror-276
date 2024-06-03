from abc import ABC, abstractmethod

from src.model.request import Request


class Interceptor(ABC):
    @abstractmethod
    def process(self, request: Request) -> Request:
        pass
