import json

from src import utils
from src.interceptor.interceptor import Interceptor
from src.model.request import Request
from src.utils import create_md_file


class MarkdownInterceptor(Interceptor):
    def process(self, request: Request):
        with open(utils.get_temp_output_file(), "r") as f:
            conversations = json.load(f)
        create_md_file(conversations)
        return request
