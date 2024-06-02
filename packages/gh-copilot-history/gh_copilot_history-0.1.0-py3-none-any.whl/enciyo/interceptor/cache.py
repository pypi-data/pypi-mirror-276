import json

from enciyo import utils
from enciyo.interceptor.interceptor import Interceptor
from enciyo.model.request import Request


class CacheInterceptor(Interceptor):
    def process(self, request: Request):
        with open(utils.get_temp_output_file(), "r") as f:
            conversations = json.load(f)

        if request.conversation.prompt != "ignore":
            conversations.append(request.conversation.to_dict())
            print(f"Conversation saved to {utils.get_temp_output_file()}")

        with open(utils.get_temp_output_file(), "w") as f:
            json.dump(conversations, f, indent=2, default=str, ensure_ascii=False)

        return request
