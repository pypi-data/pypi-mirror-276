from src import utils
from src.intercp.interceptor import Interceptor
from src.model.request import Request


class MarkdownInterceptor(Interceptor):
    def process(self, request: Request):
        conversations = utils.get_json_files()
        utils.create_md_file(conversations)
        return request
