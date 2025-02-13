
from app.services.processors.base_handler import BaseHandler
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BranchHandler(BaseHandler):
    
    def handle(self, event: str, request: dict):
        if event == '':
            pass