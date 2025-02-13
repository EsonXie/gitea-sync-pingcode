import hashlib
import re
import time
from typing import List
from app.services.pingcode_client import PingCodeClient

def generate_commit_id():
    current_time = str(time.time()).encode('utf-8')
    return hashlib.sha1(current_time).hexdigest()

def get_work_item_identification(content: str) -> List[str]:
    matchs = re.findall('#[a-zA-Z0-9]+-[0-9]+', content, re.M)
    identifiers = []
    for match in matchs:
        identifiers.append(match[1:])
    return identifiers


if __name__ == '__main__':
    
    # print(get_work_item_identification('#TEST-1 #TEST-2'))
    
    
    
    client = PingCodeClient('https://open.pingcode.com', 'nkTVCboneMqL', 'YKEWdcIZDtHnBNYFqtBuoBYz')
    products = client.SCMClient.getProducts('Gitea').get('values', None)
    product = None
    if products.__len__() == 0:
        product = client.SCMClient.createProduct('Gitea', 'git', 'Gitea')
    else:
        product = products[0]
        
    print(product)
    
    repos = client.SCMClient.getRepositories(product.get('id', None), 'eson/test4').get('values', None)
    repo = None
    if repos.__len__() == 0:
        html_url = f"http://192.168.10.229:3000/eson/test3"
        repo = client.SCMClient.createRepository(product.get('id', None), {
            'name': 'test2',
            'full_name': 'eson/test3',
            'html_url': html_url,
            'branches_url': f'{html_url}/src/branch/{{branch}}',
            'commits_url': f'{html_url}/commit/{{sha}}',
            'compare_url': f'{html_url}/compare/{{base}}...{{head}}',
            'pulls_url': f'{html_url}/pulls/{{number}}'
        })
    else:
        repo = repos[0]
        html_url = f"http://192.168.10.229:3000/eson/test3"
        repo['html_url'] = html_url
        repo['branches_url']= f'{html_url}/src/branch/{{branch}}'
        repo['commits_url']= f'{html_url}/commit/{{sha}}'
        repo['compare_url']= f'{html_url}/compare/{{base}}...{{head}}'
        repo['pulls_url']= f'{html_url}/pulls/{{number}}'
        repo = client.SCMClient.putRepository(product.get('id', None), repo.get('id'), repo)
        
    print(repo)
    
    # branches = client.SCMClient.getRepositoryBranches(product.get('id', None) ,repo.get('id', None)).get('values', None)
    # branch = None
    # if branches.__len__() == 0:
    #     branch = client.SCMClient.createRepositoryBranch(product.get('id', None), repo.get('id', None), {
    #         'name': 'eson-test',
    #         'sender_name': 'eson-test'
    #     })
    # else:
    #     branch = branches[0]
    
    # print(branch)
    
    # workerItems = client.ProjectClient.getWorkItemsByIdentifier('TEST-2').get('values', None)[0]
    # print(workerItems)
    
    # print(uuid.uuid4().hex)
    # 1403018919
    # 1732616259
    # int(datetime.timestamp(datetime.now()))
    
    
    # commit = {
    #     'sha': generate_commit_id(),
    #     'message': 'message-test',
    #     'committed_at': int(time.time() - 5),
    #     'committer_name': 'eson-test',
    #     'tree_id': generate_commit_id(),
    #     'files_added': ['files_added'],
    #     'files_removed': ['files_removed'],
    #     'files_modified': ['files_modified'],
    #     'work_item_identifiers': ['TEST-1']
    # }
    # print('----------------commit提交数据----------------')
    
    # print(commit)
    
    # print('----------------commit提交返回数据----------------')
    # print(client.SCMClient.createCommit(commit))
    # print('----------------commit提交引用返回数据----------------')
    # print(client.SCMClient.createRef(product_id=product.get('id', None), repository_id=repo.get('id', None), branch_id=branch.get('id', None), sha=commit.get('sha', None)))
    # print('----------------工作项数据----------------')
    # print(client.SCMClient.getCommits(worker_item_id='67458d236fad4a954cfd40e3'))
    
    
    # print(client.SCMClient.createRepositoryBranch(product.get('id', None), repo.get('id', None), {
    #         'name': 'eson-test2',
    #         'sender_name': 'eson-test2',
    #         'work_item_identifiers':['TEST-1']
    #     }))
    
    
    
    # print(client.SCMClient.createPullRequest(product.get('id', None), repo.get('id', None), {
    #     'title': 'title-test',
    #     'number': 1,
    #     'creator_name': 'eson-test',
    #     'description': 'description-test',
    #     'source_branch_id': branches[0].get('id', None),
    #     'target_branch_id': branches[1].get('id', None),
    #     'work_item_identifiers': ['TEST-1'],
    #     'status': 'open'
    # }))