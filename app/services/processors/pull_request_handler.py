from datetime import datetime
import logging

from app.dependencies import get_giteapy_client, get_pingcode_client
from app.services.processors.base_handler import BaseHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PullRequestHandler(BaseHandler):
    def handle(self, event: str, request: dict):
        if event == 'pull_request':
            # 创建pr
            if request['action'] == 'opened' or request['action'] == 'synchronized' or request['action'] == 'edited' or request['action'] == 'closed' or True:
                pull_request = request['pull_request']
                work_items = self.get_work_item_identification(f'{pull_request["title"]}\n{pull_request["body"]}')
                
                if len(work_items) != 0:
                    
                    client = get_pingcode_client()
                    
                    product_id = self.get_product_id()
                    target_repository_id = self.get_repository_id(pull_request['base']['repo']['full_name'], pull_request['base']['repo']['html_url'])
                    
                    pull_requests = client.SCMClient.getPullRequests(product_id, target_repository_id, pull_request['number']).get('values', [])
                    current_pull_request = None
                    if len(pull_requests) != 0:
                        current_pull_request = pull_requests[0]
                    
                    if current_pull_request is None:
                        source_branch_id = self.get_branch_id(pull_request['head']['repo']['full_name'], pull_request['head']['ref'], pull_request['user']['username'])
                        target_branch_id = self.get_branch_id(pull_request['base']['repo']['full_name'], pull_request['base']['ref'], pull_request['user']['username'])
                        
                        current_pull_request = client.SCMClient.createPullRequest(product_id, target_repository_id, {
                            'title': pull_request['title'],
                            'number': pull_request['number'],
                            'creator_name': pull_request['user']['username'],
                            'description': pull_request['body'],
                            'source_branch_id': source_branch_id,
                            'target_branch_id': target_branch_id,
                            'status': pull_request['state'],
                            'comments_count': pull_request['comments'],
                            'review_comments_count': pull_request['review_comments'],
                            'commits_count': self.get_commit_count(request['repository']['owner']['username'], request['repository']['name'], request['number']),
                            'work_item_identifiers': work_items
                        })
                        
                    else:
                        source_branch_id = self.get_branch_id(pull_request['head']['repo']['full_name'], pull_request['head']['ref'], pull_request['user']['username'])
                        target_branch_id = self.get_branch_id(pull_request['base']['repo']['full_name'], pull_request['base']['ref'], pull_request['user']['username'])
                        
                        date_format = "%Y-%m-%dT%H:%M:%SZ"
                        current_pull_request = client.SCMClient.putPullRequest(product_id, target_repository_id, current_pull_request['id'] , {
                            'title': pull_request['title'],
                            'creator_name': pull_request['user']['username'],
                            'description': pull_request['body'],
                            'source_branch_id': source_branch_id,
                            'target_branch_id': target_branch_id,
                            'status': 'merged' if pull_request['state'] == 'closed' and pull_request['merged'] else pull_request['state'],
                            'merged_at': int(datetime.strptime(pull_request['merged_at'], date_format).timestamp()) if pull_request['state'] == 'closed' and pull_request['merged'] else None,
                            'merged_commit_sha': pull_request['merge_commit_sha'] if pull_request['state'] == 'closed' and pull_request['merged'] else None,
                            'merged_by_name': pull_request['merged_by']['username'] if pull_request['state'] == 'closed' and pull_request['merged'] else None,
                            'comments_count': pull_request['comments'],
                            'review_comments_count': pull_request['review_comments'],
                            'commits_count': self.get_commit_count(request['repository']['owner']['username'], request['repository']['name'], request['number']),
                            'work_item_identifiers': work_items
                        })
        return super().handle(event, request)
    
    
    def get_commit_count(self, owner, repo, index) -> int:
        client = get_giteapy_client()
        
        commits = client.repository_api.repo_get_pull_request_commits_with_http_info('eson', 'test', 2, limit=1)
        result = len(commits[0])
        if commits[2].get('X-HasMore') == 'true':
            result = int(commits[2].get('X-Total-Count'))
        
        return result
