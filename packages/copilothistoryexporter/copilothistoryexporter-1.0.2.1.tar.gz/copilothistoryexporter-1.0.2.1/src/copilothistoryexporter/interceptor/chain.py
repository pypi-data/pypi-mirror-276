from copilothistoryexporter.interceptor.cache import CacheInterceptor
from copilothistoryexporter.interceptor.markdown import MarkdownInterceptor
from copilothistoryexporter.interceptor.vote import VoteInterceptor
from copilothistoryexporter.model.request import Request


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
