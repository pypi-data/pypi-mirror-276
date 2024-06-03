from src.intercp.cache import CacheInterceptor
from src.intercp.markdown import MarkdownInterceptor
from src.intercp.vote import VoteInterceptor
from src.model.request import Request

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
