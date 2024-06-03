from copilothistoryexporter import utils
from copilothistoryexporter.intercp.interceptor import Interceptor
from copilothistoryexporter.model.request import Request


class MarkdownInterceptor(Interceptor):
    def process(self, request: Request):
        conversations = utils.get_json_files()
        utils.create_md_file(conversations)
        return request
