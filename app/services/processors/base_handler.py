# base_handler.py
from abc import ABC, abstractmethod
import logging
import re
from typing import List

from cachetools import TTLCache, cached
from app.dependencies import get_giteapy_client, get_pingcode_client

cache = TTLCache(maxsize=100, ttl=3600)


class BaseHandler(ABC):
    def __init__(self, successor=None):
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._successor = successor

    @abstractmethod
    def handle(self, event: str, request: dict):
        if self._successor:
            self.logger.info(f"Handler: {self.__class__.__name__} is handling the request")
            return self._successor.handle(event ,request)
        return None
    
    def get_work_item_identification(self, content: str) -> List[str]:
        matchs = re.findall('#[a-zA-Z0-9]+-[0-9]+', content, re.M)
        identifiers = []
        for match in matchs:
            identifiers.append(match[1:])
        return list(set(identifiers))
        
    @cached(cache, key=lambda self: 'product')
    def get_product_id(self):
        client = get_pingcode_client()
        products = client.SCMClient.getProducts('Gitea').get('values', None)
        product = None
        if products.__len__() == 0:
            product = client.SCMClient.createProduct('Gitea', 'git', 'Gitea')
        else:
            product = products[0]
        
        return product.get('id', None)
    
    @cached(cache, key=lambda self, full_name, html_url: f'repo-{full_name}')
    def get_repository_id(self, full_name: str, html_url: str):
        client = get_pingcode_client()
        product_id = self.get_product_id()
        repos = client.SCMClient.getRepositories(product_id, full_name).get('values', None)
        repo = None
        if len(repos) == 0:
            repo = client.SCMClient.createRepository(product_id, {
                'name': full_name.split('/')[-1],
                'full_name': full_name,
                'html_url': html_url,
                'branches_url': f'{html_url}/src/branch/{{branch}}',
                'commits_url': f'{html_url}/commit/{{sha}}',
                'compare_url': f'{html_url}/compare/{{base}}...{{head}}',
                'pulls_url': f'{html_url}/pulls/{{number}}',
            })
                                                     
        else:
            repo = repos[0]
            if repo.get('html_url', None) != html_url and html_url != None:
                repo['html_url'] = html_url
                repo['branches_url']= f'{html_url}/src/branch/{{branch}}'
                repo['commits_url']= f'{html_url}/commit/{{sha}}'
                repo['compare_url']= f'{html_url}/compare/{{base}}...{{head}}'
                repo['pulls_url']= f'{html_url}/pulls/{{number}}'
                repo = client.SCMClient.putRepository(product_id, repo.get('id'), repo)
        return repo.get('id', None)
    
    @cached(cache, key=lambda self, repo_name, branch_name, sender_name: f'branch-{repo_name}-{branch_name}')
    def get_branch_id(self, repo_name: str, branch_name: str, sender_name: str):
        client = get_pingcode_client()
        product_id = self.get_product_id()
        repo_id = self.get_repository_id(full_name=repo_name, html_url=None)
        branches = client.SCMClient.getRepositoryBranches(product_id, repo_id, branch_name).get('values', None)
        
        branch = None
        if len(branches) == 0:
            worker_items = self.get_work_item_identification(branch_name)
            branch = client.SCMClient.createRepositoryBranch(product_id, repo_id, {
                'name': branch_name,
                'sender_name': sender_name,
                'work_item_identifiers': worker_items
            })
        else:
            branch = branches[0]
        return branch.get('id', None)