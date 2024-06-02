import json

from enciyo import utils
from enciyo.interceptor.interceptor import Interceptor
from enciyo.model.request import Request
from enciyo.utils import create_md_file


class MarkdownInterceptor(Interceptor):
    def process(self, request: Request):
        with open(utils.get_temp_output_file(), "r") as f:
            conversations = json.load(f)
        create_md_file(conversations)
        return request
