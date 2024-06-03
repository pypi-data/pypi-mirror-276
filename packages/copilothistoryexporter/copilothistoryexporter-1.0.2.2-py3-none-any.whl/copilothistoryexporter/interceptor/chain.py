from src.copilothistoryexporter.interceptor.cache import CacheInterceptor
from src.copilothistoryexporter.interceptor.markdown import MarkdownInterceptor
from src.copilothistoryexporter.interceptor.vote import VoteInterceptor
from src.copilothistoryexporter.model.request import Request


class InterceptorChain:
    def __init__(self):
        self.interceptors = [
            VoteInterceptor(),
            CacheInterceptor(),
            MarkdownInterceptor()
        ]

    def execute(self, request: Request):
        try:
            for interceptor in self.interceptors:
                request = interceptor.process(request)
        except RuntimeError:
            pass
