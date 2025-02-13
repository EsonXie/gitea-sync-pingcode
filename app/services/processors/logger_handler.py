import json
from .base_handler import BaseHandler

class LoggerHandler(BaseHandler):
    def handle(self, event: str, request: dict):
        self.logger.info(f"Event:{event}\nRequest body: {json.dumps(request)}")
        return super().handle(event ,request)