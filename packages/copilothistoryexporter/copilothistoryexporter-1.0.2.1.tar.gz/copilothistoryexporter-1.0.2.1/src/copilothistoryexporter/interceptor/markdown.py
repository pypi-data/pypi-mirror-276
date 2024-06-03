from copilothistoryexporter import utils
from copilothistoryexporter.interceptor.interceptor import Interceptor
from copilothistoryexporter.model.request import Request
from copilothistoryexporter.utils import create_md_file


class MarkdownInterceptor(Interceptor):
    def process(self, request: Request):
        conversations = utils.get_json_files()
        create_md_file(conversations)
        return request
