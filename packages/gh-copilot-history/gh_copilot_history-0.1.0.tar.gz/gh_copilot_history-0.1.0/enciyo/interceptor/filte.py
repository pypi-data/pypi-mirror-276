from enciyo.interceptor.interceptor import Interceptor
from enciyo.model.request import Request
from enciyo.utils import initialize_directories_and_files


class FileInterceptor(Interceptor):
    def process(self, request: Request):
        initialize_directories_and_files()
        return request
