import re

from mitmproxy import http

from enciyo.interceptor import chain
from enciyo.model import Conversation
from enciyo.model.request import Request

LISTEN_URL = "https://api.githubcopilot.com/chat/completions"
LISTEN_URL_RATING = "https://copilot-telemetry.githubusercontent.com/telemetry"


def get_message_from_response(data) -> list[Conversation]:
    user_contents = [message['content'] for message in data['messages'] if message['role'] == 'user']
    if user_contents.__len__() == 1 and data.get("intent_content", None) is None:
        text = user_contents[0].replace("Consider the following conversation history:\n", "")
        pattern = re.compile(r"\d\) User: (.*?)\n")
        split_text = re.split(pattern, text)
        user_response = split_text[1::2]
        copilot_response = [response.replace("GitHub Copilot: ", "").rstrip("\n\n") for response in split_text[::2]]
        copilot_response = [response for response in copilot_response if response != ""]
        return [Conversation(user_response[i], copilot_response[i]) for i in range(len(user_response))]
    else:
        return None


def request(flow: http.HTTPFlow) -> None:
    if flow.request.pretty_url == LISTEN_URL:
        data = flow.request.json()
        conversation = get_message_from_response(data)[-1]
        if conversation is not None and Conversation == type(conversation):
            chain.execute(Request(flow, conversation))


addons = [request]
