from datetime import datetime
import logging
from typing import List
from app import dependencies

from .base_handler import BaseHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CommitHandler(BaseHandler):
    def handle(self, event: str, request: dict):
        
        if event == 'push':
            
            (repo_name,)=request['repository']['full_name'], 
            (repo_html_url,)=request.get('repository').get('html_url', None),
            (branch_name,)=request.get('ref').replace('refs/heads/', ''),
            (sender_name,)=request['pusher']['username'],
            
            
            product_id = self.get_product_id()
            repository_id = self.get_repository_id(repo_name, repo_html_url)
            branch_id = self.get_branch_id(repo_name, branch_name, sender_name)
            
            commits = request.get('commits')
            for commit in commits:
                message = commit.get("message")
                worker_items = self.get_work_item_identification(message)
                if len(worker_items) > 0:
                    logger.info(f'Worker item: {worker_items}')
                    # self.send_to_worker(worker_item)
                    date_format = "%Y-%m-%dT%H:%M:%SZ"
                    commit = {
                        'sha': commit['id'],
                        'message': commit['message'],
                        'committed_at': int(datetime.strptime(commit['timestamp'], date_format).timestamp()),
                        'committer_name': commit['committer']['name'],
                        # 'tree_id': generate_commit_id(),
                        'files_added': commit['added'],
                        'files_removed': commit['removed'],
                        'files_modified': commit['modified'],
                        'work_item_identifiers': worker_items
                    }
                    self.createCommit(product_id=product_id, 
                                      repository_id=repository_id,
                                      branch_id=branch_id,
                                      commit=commit)
                # logger.info(f'Commit message: {commit.get("message")}')
        
        return super().handle(event, request)
    
    def createCommit(self, 
                     product_id: str,
                     repository_id: str,
                     branch_id: str,
                     commit: dict):
        
        client = dependencies.get_pingcode_client()
        resp = client.SCMClient.createCommit(commit)
        commit_id = resp.get('sha', None)
        
        client.SCMClient.createRef(product_id, 
                                   repository_id, 
                                   branch_id, 
                                   commit_id)
        
        return commit_id
    
    def relate_work_item_to_branch(self, product_id: str, repository_id: str, branch_name: str, work_item_identifiers: List[str]):
        
        # client = dependencies.get_pingcode_client()
        # branchs = client.SCMClient.getRepositoryBranches(product_id, repository_id, branch_name).get('values', [])
        # branch = None
        # if len(branchs) == 0:
        #     branch = client.SCMClient.createRepositoryBranch(product_id, repository_id, branch_name)
        # else:
        #     branch = branchs[0]
        
        # branch_work_items = branch.get('work_items', [])
        
        # relate_items = [{branch_item['identifier'] for branch_item in branch_work_items}]
        
        # needToRelateItems = [item for item in work_item_identifiers if item not in relate_items]
        
        # print(needToRelateItems)
        pass
        
        
        