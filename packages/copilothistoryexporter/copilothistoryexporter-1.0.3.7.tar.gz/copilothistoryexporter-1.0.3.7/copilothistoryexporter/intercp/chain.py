from copilothistoryexporter.intercp.cache import CacheInterceptor
from copilothistoryexporter.intercp.markdown import MarkdownInterceptor
from copilothistoryexporter.intercp.vote import VoteInterceptor
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
