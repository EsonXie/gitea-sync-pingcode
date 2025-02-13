from urllib.request import BaseHandler
from cachetools import TTLCache, cached
from app.services.gitea_client import GiteaClient
from app.services.pingcode_client import PingCodeClient
from .config import config

cache = TTLCache(maxsize=100, ttl=3600)

@cached(cache, key=lambda: 'pingcode-client')
def get_pingcode_client() -> PingCodeClient:
    return PingCodeClient(config.pingcode['base_url'], config.pingcode['client_id'], config.pingcode['client_secret'])

@cached(cache, key=lambda: 'gitea-client')
def get_giteapy_client() -> GiteaClient:
    return GiteaClient(config.gitea['base_url'], config.gitea['access_token'])

@cached(cache, key=lambda: 'handler')
def get_handler() -> BaseHandler:
    from app.services.processors.logger_handler import LoggerHandler
    from app.services.processors.commit_handler import CommitHandler
    from app.services.processors.pull_request_handler import PullRequestHandler

    pullrequesthandler = PullRequestHandler()
    commithandler = CommitHandler(pullrequesthandler)
    logger = LoggerHandler(commithandler)
    return logger