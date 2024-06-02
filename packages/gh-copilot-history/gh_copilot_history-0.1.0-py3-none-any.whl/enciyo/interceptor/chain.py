from enciyo.interceptor.cache import CacheInterceptor
from enciyo.interceptor.filte import FileInterceptor
from enciyo.interceptor.markdown import MarkdownInterceptor
from enciyo.interceptor.vote import VoteInterceptor
from enciyo.model.request import Request


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
