import json

from enciyo import utils
from enciyo.interceptor.interceptor import Interceptor
from enciyo.model.request import Request


class VoteInterceptor(Interceptor):
    def process(self, request: Request):
        prompt = request.conversation.prompt
        if prompt == "vote:good" or prompt == "vote:bad":
            with open(utils.get_temp_output_file(), "r") as f:
                conversations = json.load(f)
            conversations[-1]["rating"] = "***" if prompt == "vote:good" else "*"
            with open(utils.get_temp_output_file(), "w") as f:
                json.dump(conversations, f)
            request.conversation.prompt = "ignore"

        return request
