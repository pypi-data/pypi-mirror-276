from src.interceptor.interceptor import Interceptor
from src.model.request import Request
from src.utils import initialize_directories_and_files


class FileInterceptor(Interceptor):
    def process(self, request: Request):
        initialize_directories_and_files()
        return request
