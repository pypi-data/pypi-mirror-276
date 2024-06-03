from src.copilothistoryexporter import utils
from src.copilothistoryexporter.interceptor.interceptor import Interceptor
from src.copilothistoryexporter.model.request import Request


class VoteInterceptor(Interceptor):
    def process(self, request: Request):
        prompt = request.conversation.prompt
        if prompt == "vote:good" or prompt == "vote:bad":
            conversations = utils.get_json_files()
            conversations[-1]["rating"] = "***" if prompt == "vote:good" else "*"
            utils.write_to_json_file(conversations)
            request.conversation.prompt = "ignore"
        return request
