from src.copilothistoryexporter import utils
from src.copilothistoryexporter.interceptor.interceptor import Interceptor
from src.copilothistoryexporter.model.request import Request
from src.copilothistoryexporter.utils import create_md_file


class MarkdownInterceptor(Interceptor):
    def process(self, request: Request):
        conversations = utils.get_json_files()
        create_md_file(conversations)
        return request
