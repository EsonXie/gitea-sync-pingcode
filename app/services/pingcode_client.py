import requests

class PingCodeBaseClient:
    
    def __init__(self, base_url: str, client_id: str, client_secret: str):
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        
    def getToken(self):
        uri = self.base_url + '/v1/auth/token?grant_type=client_credentials&client_id=' + self.client_id + '&&client_secret=' + self.client_secret
        res_data = requests.get(uri).json()
        if res_data.get('access_token', None):
            return res_data.get('access_token', None)
        else:
            raise Exception("Invalid client_id or client_secret")
        
    def get(self, path: str, headers: dict, params: dict = None):
        resp = requests.get(self.base_url + path, headers=headers, params=params)
        return resp.json()
         
    def post(self, path: str, headers: dict, data: dict):
        filtered_data = {k: v for k, v in data.items() if v is not None}
        resp = requests.post(self.base_url + path, headers=headers, json=filtered_data)
        return resp.json()
    
    def put(self, path: str, headers: dict, data: dict):
        filtered_data = {k: v for k, v in data.items() if v is not None}
        resp = requests.put(self.base_url + path, headers=headers, json=filtered_data)
        return resp.json()
    def delete(self, path: str, headers: dict):
        resp = requests.delete(self.base_url + path, headers=headers)
        return resp.json()
        
        
class PingCodeClient:
    def __init__(self, base_url: str, client_id: str, client_secret: str):
        self.baseClient = PingCodeBaseClient(base_url, client_id, client_secret)
        self.SCMClient = SCMClient(self.baseClient)
        self.ProjectClient = ProjectClient(self.baseClient)
        

class SCMClient:
    def __init__(self, baseClient: PingCodeBaseClient):
        self.baseClient = baseClient
        
    
    def getHeaders(self) -> dict:
        token = self.baseClient.getToken()
        return {'Authorization': 'Bearer ' + token}
    
    def getProducts(self, name: str):
        headers = self.getHeaders()
        return self.baseClient.get(f'/v1/scm/products', headers=headers, params={'name': name})
    
    def getProductById(self, product_id: str):
        headers = self.getHeaders()
        return self.baseClient.get(f'/v1/scm/products/{product_id}', headers=headers)
    
    def createProduct(self, name: str, type: str, description: str):
        types = ['github', 'gitlab', 'bitbucket', 'coding.net', 'gogs', 'git', 'svn', 'other']
        if(type not in types):
            raise Exception("Invalid type")
        headers = self.getHeaders()
        data = {'name': name, 'type': type, 'description': description}
        return self.baseClient.post('/v1/scm/products', headers=headers, data=data)
    
    def putProduct(self, product_id: str, name: str, type: str, description: str):
        types = ['github', 'gitlab', 'bitbucket', 'coding.net', 'gogs', 'git', 'svn', 'other']
        if(type not in types):
            raise Exception("Invalid type")
        headers = self.getHeaders()
        data = {'name': name, 'type': type, 'description': description}
        return self.baseClient.post(f'/v1/scm/products/{product_id}', headers=headers, data=data)
    
    # def deleteProduct(self, product_id: str):
    #     headers = self.getHeaders()
    #     return self.baseClient.delete(f'/v1/scm/products/{product_id}', headers=headers)
        
    def getProductUsers(self, product_id: str, name: str):
        headers = self.getHeaders()
        return self.baseClient.get(f'/v1/scm/products/{product_id}/users', params={'name': name} , headers=headers)
    def getProductUserById(self, product_id: str, user_id: str):
        headers = self.getHeaders()
        return self.baseClient.get(f'/v1/scm/products/{product_id}/users/{user_id}', headers=headers)
    def createProductUser(self, product_id: str, name: str, display_name: str, html_url: str, avatar_url: str):
        headers = self.getHeaders()
        data = {'name': name, 'display_name': display_name, 'html_url': html_url, 'avatar_url': avatar_url}
        return self.baseClient.post(f'/v1/scm/products/{product_id}/users', headers=headers, data=data)
    def putProductUser(self, product_id: str, user_id: str, name: str, display_name: str, html_url: str, avatar_url: str):
        headers = self.getHeaders()
        data = {'name': name, 'display_name': display_name, 'html_url': html_url, 'avatar_url': avatar_url}
        return self.baseClient.put(f'/v1/scm/products/{product_id}/users/{user_id}', headers=headers, data=data)
    
    
    def getRepositories(self, product_id: str, full_name: str = None):
        headers = self.getHeaders()
        return self.baseClient.get(f'/v1/scm/products/{product_id}/repositories', params={'full_name': full_name}, headers=headers)
    def getRepositoryById(self, product_id: str, repository_id: str):
        headers = self.getHeaders()
        return self.baseClient.get(f'/v1/scm/products/{product_id}/repositories/{repository_id}', headers=headers)
    def createRepository(self, product_id: str, repo: dict[str, str]):
        """
        创建仓库

        :param product_id: 产品 ID
        :param repo: 仓库信息字典，包含以下字段：
            - name: str
            - full_name: str
            - description: str
            - is_fork: bool
            - is_private: bool
            - owner_name: str
            - html_url: str
            - branches_url: str
            - commits_url: str
            - compare_url: str
            - pulls_url: str
        """
        headers = self.getHeaders()
        data = {
            'name': repo.get('name', None), 
            'full_name': repo.get('full_name', None), 
            'description': repo.get('description', None), 
            'html_url': repo.get('html_url', None), 
            'clone_url': repo.get('clone_url', None), 
            'ssh_url': repo.get('ssh_url', None), 
            'svn_url': repo.get('svn_url', None)
        }
        return self.baseClient.post(f'/v1/scm/products/{product_id}/repositories', headers=headers, data=data)
    def putRepository(self, product_id: str, repository_id: str, repo: dict[str, str]):
        """
        更新仓库
        
        :param product_id: 产品 ID
        :param repository_id: 仓库 ID
        :param repo: 仓库信息字典，包含以下字段：
            - name: str
            - full_name: str
            - description: str
            - html_url: str
            - branches_url: str
            - commits_url: str
            - compare_url: str
            - pulls_url: str
        """
        headers = self.getHeaders()
        data = {
            'name': repo.get('name', None), 
            'full_name': repo.get('full_name', None), 
            'description': repo.get('description', None), 
            'html_url': repo.get('html_url', None), 
            'branches_url': repo.get('branches_url', None), 
            'commits_url': repo.get('commits_url', None), 
            'compare_url': repo.get('compare_url', None),
            'pulls_url': repo.get('pulls_url', None)
        }
        return self.baseClient.put(f'/v1/scm/products/{product_id}/repositories/{repository_id}', headers=headers, data=data)
    
    def getRepositoryBranches(self, product_id: str, repository_id: str, name: str = None):
        headers = self.getHeaders()
        return self.baseClient.get(f'/v1/scm/products/{product_id}/repositories/{repository_id}/branches', params={'name': name}, headers=headers)
    def createRepositoryBranch(self, product_id: str, repository_id: str, branch: dict):
        """
        创建分支
        
        
        :param product_id: 产品 ID
        :param repository_id: 仓库 ID
        :param branch: 分支信息字典，包含以下字段：
            - name: str
            - sender_name: str
            - is_default: bool
            - work_item_identifiers: List[str]
        """
        headers = self.getHeaders()
        data = {
            'name': branch.get('name', None), 
            'sender_name': branch.get('sender_name', None),
            'is_default': branch.get('is_default', None),
            'work_item_identifiers': branch.get('work_item_identifiers', None)
        }
        return self.baseClient.post(f'/v1/scm/products/{product_id}/repositories/{repository_id}/branches', headers=headers, data=data)
    def deleteRepositoryBranch(self, product_id: str, repository_id: str, branch_id: str):
        headers = self.getHeaders()
        return self.baseClient.delete(f'/v1/scm/products/{product_id}/repositories/{repository_id}/branches/{branch_id}', headers=headers)
    
    def createCommit(self, commit: dict):
        """
        创建提交
        
        :param commit: 提交信息字典，包含以下字段：
            - sha: str
            - message: str
            - committer_name: str
            - committer_at: int
            - tree_id: str
            - files_added: List[str]
            - files_removed: List[str]
            - files_modified: List[str]
            - work_item_identifiers: List[str]
        """
        headers = self.getHeaders()
        return self.baseClient.post(f'/v1/scm/commits', headers=headers, data=commit)
    
    def getCommits(self, sha:str = None, worker_item_id:str = None):
        headers = self.getHeaders()
        return self.baseClient.get(f'/v1/scm/commits', headers=headers, params={'sha': sha, 'work_item_id': worker_item_id})
    
    def createRef(self, product_id: str, repository_id: str, branch_id: str, sha: str):
        headers = self.getHeaders()
        return self.baseClient.post(f'/v1/scm/products/{product_id}/repositories/{repository_id}/refs', headers=headers, 
                                    data={
                                        'sha': sha, 
                                        'meta_type': 'branch',
                                        'meta_id': branch_id
                                        })
        
    def getRefs(self, product_id: str, repository_id: str, branch_id: str):
        headers = self.getHeaders()
        return self.baseClient.get(f'/v1/scm/products/{product_id}/repositories/{repository_id}/refs', headers=headers, params={'meta_type': 'branch', 'meta_id': branch_id})
        
    def getPullRequests(self, product_id: str, repository_id: str, number: int = None, worker_item_id: str = None):
        headers = self.getHeaders()
        return self.baseClient.get(f'/v1/scm/products/{product_id}/repositories/{repository_id}/pull_requests', headers=headers, params={'number': number, 'work_item_id': worker_item_id})
        
    def createPullRequest(self, product_id: str, repository_id: str, pull_request: dict):
        """
        创建拉取请求
        
        :param product_id: 产品 ID
        :param repository_id: 仓库 ID
        :param pull_request: 拉取请求信息字典，包含以下字段：
            - title: str
            - number: int
            - creator_name: str
            - source_branch_id: str
            - target_branch_id: str
            - status: str
            - description: str
            - merged_at: str
            - merged_commit_sha: str
            - merged_by_name: str
            - comments_count: int
            - review_comments_count: int
            - commits_count: int
            - additions_count: int
            - deletions_count: int
            - changed_files_count: int
            - work_item_identifiers: List[str]
        """
        headers = self.getHeaders()
        return self.baseClient.post(f'/v1/scm/products/{product_id}/repositories/{repository_id}/pull_requests', headers=headers, data=pull_request)
        
    def putPullRequest(self, product_id: str, repository_id: str, pull_request_id: str, pull_request: dict):
        """
        更新拉取请求
        
        :param product_id: 产品 ID
        :param repository_id: 仓库 ID
        :param pull_request_id: 拉取请求 ID
        :param pull_request: 拉取请求信息字典，包含以下字段：
            - title: str
            - number: int
            - creator_name: str
            - source_branch_id: str
            - target_branch_id: str
            - status: str (open, closed, merged)
            - description: str
            - merged_at: str
            - merged_commit_sha: str
            - merged_by_name: str
            - comments_count: int
            - review_comments_count: int
            - commits_count: int
            - additions_count: int
            - deletions_count: int
            - changed_files_count: int
            - work_item_identifiers: List[str]
        """
        headers = self.getHeaders()
        return self.baseClient.put(f'/v1/scm/products/{product_id}/repositories/{repository_id}/pull_requests/{pull_request_id}', headers=headers, data=pull_request)
    
class ProjectClient:
    
    def __init__(self, baseClient: PingCodeBaseClient):
        self.baseClient = baseClient
        
    
    def getHeaders(self) -> dict:
        token = self.baseClient.getToken()
        return {'Authorization': 'Bearer ' + token}
    
    def getWorkItemsByIdentifier(self, identifier: str):
        headers = self.getHeaders()
        return self.baseClient.get(f'/v1/project/work_items', headers=headers, params={'identifier': identifier})
    