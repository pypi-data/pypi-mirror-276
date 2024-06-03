from src.interceptor.cache import CacheInterceptor
from src.interceptor.filte import FileInterceptor
from src.interceptor.markdown import MarkdownInterceptor
from src.interceptor.vote import VoteInterceptor
from src.model.request import Request


class InterceptorChain:
    def __init__(self):
        self.interceptors = [
            FileInterceptor(),
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
