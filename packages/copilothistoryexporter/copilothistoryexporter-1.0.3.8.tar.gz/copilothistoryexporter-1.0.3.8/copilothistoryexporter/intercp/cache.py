from copilothistoryexporter import utils
from copilothistoryexporter.intercp.interceptor import Interceptor
from copilothistoryexporter.model.request import Request


class CacheInterceptor(Interceptor):
    def process(self, request: Request):
        conversations = utils.get_json_files()
        if request.conversation.prompt != "ignore":
            conversations.append(request.conversation.to_dict())
            print("Cache updated")

        utils.write_to_json_file(conversations)

        return request
