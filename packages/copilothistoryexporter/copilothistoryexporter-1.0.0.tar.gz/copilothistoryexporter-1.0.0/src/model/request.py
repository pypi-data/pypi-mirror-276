from mitmproxy import http

from src.model import Conversation


class Request:
    def __init__(self, flow: http.HTTPFlow, conversation: Conversation):
        self.flow = flow
        self.conversation = conversation
