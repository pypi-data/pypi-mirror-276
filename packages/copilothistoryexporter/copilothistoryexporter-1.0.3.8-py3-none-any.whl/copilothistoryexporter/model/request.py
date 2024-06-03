from mitmproxy import http

from copilothistoryexporter.model.conversation import Conversation


class Request:
    def __init__(self, flow: http.HTTPFlow, conversation: Conversation):
        self.flow = flow
        self.conversation = conversation
